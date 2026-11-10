"""Filesystem mailbox primitives. See README for concurrency limits."""
from __future__ import annotations

import os
import fcntl
from contextlib import contextmanager
import time
import uuid
from pathlib import Path
from typing import NamedTuple


class Layout(NamedTuple):
    tmp: Path
    new: Path
    cur: Path


class DeliveryResult(NamedTuple):
    path: Path
    delivered: bool  # False: this call observed an already-delivered key (no-op)


class ClaimResult(NamedTuple):
    path: Path | None
    claimed: bool  # True: this call is the exclusive claimant, apply the effect


def ensure_layout(root: Path) -> Layout:
    """Create (idempotently) and return the tmp/new/cur triad under ``root``."""
    layout = Layout(tmp=root / "tmp", new=root / "new", cur=root / "cur")
    for directory in layout:
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    return layout


def _safe_key(key: str) -> str:
    if not key or "/" in key or "\x00" in key or key in {".", ".."}:
        raise ValueError(f"unsafe idempotency key: {key!r}")
    return key


def _unique_tmp_name() -> str:
    # qmail maildir(5)-style uniqueness: time + pid + random -- collisions
    # between deliver() calls in the same process are still excluded by
    # uuid4, and a name is only ever used once (never reused after cleanup).
    return f"{time.time_ns()}.{os.getpid()}.{uuid.uuid4().hex[:12]}"


def _deliver(root: Path, key: str, payload: bytes) -> DeliveryResult:
    """Deliver ``payload`` under idempotency ``key``; a repeat delivery is a no-op.

    Returns the path of the message (in ``new/`` if pending, ``cur/`` if a
    consumer already claimed it before this call observed it) and whether
    THIS call is the one that delivered it.
    """
    key = _safe_key(key)
    layout = ensure_layout(root)
    new_path = layout.new / key
    cur_path = layout.cur / key
    if cur_path.exists():
        return DeliveryResult(path=cur_path, delivered=False)
    if new_path.exists():
        return DeliveryResult(path=new_path, delivered=False)

    tmp_path = layout.tmp / _unique_tmp_name()
    fd = os.open(tmp_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        view = memoryview(payload)
        while view:
            written = os.write(fd, view)
            if written <= 0:
                raise OSError("short write")
            view = view[written:]
        os.fsync(fd)
    finally:
        os.close(fd)

    try:
        os.link(tmp_path, new_path)
    except FileExistsError:
        # Lost a race with a concurrent deliver() of the same key: the
        # winner's payload is the delivered message, ours is discarded.
        return DeliveryResult(path=new_path, delivered=False)
    finally:
        tmp_path.unlink(missing_ok=True)
    return DeliveryResult(path=new_path, delivered=True)


def list_pending(root: Path) -> list[str]:
    """Keys currently sitting in ``new/`` (delivered, not yet claimed)."""
    layout = ensure_layout(root)
    return sorted(entry.name for entry in layout.new.iterdir() if entry.is_file())


def _claim(root: Path, key: str) -> ClaimResult:
    """Claim ``key`` exclusively, or learn it was already claimed / never delivered.

    ``claimed=True`` means this call moved the message and owns the one
    right to apply its effect. ``claimed=False`` with a path means someone
    else already claimed it (idempotent re-claim: skip the effect).
    ``claimed=False`` with ``path=None`` means the key was never delivered.
    """
    key = _safe_key(key)
    layout = ensure_layout(root)
    new_path = layout.new / key
    cur_path = layout.cur / key
    try:
        os.rename(new_path, cur_path)
    except FileNotFoundError:
        if cur_path.exists():
            return ClaimResult(path=cur_path, claimed=False)
        return ClaimResult(path=None, claimed=False)
    return ClaimResult(path=cur_path, claimed=True)


def read(path: Path) -> bytes:
    return path.read_bytes()


def sweep_stale_tmp(root: Path, max_age_seconds: float) -> list[Path]:
    """Remove ``tmp/`` entries older than ``max_age_seconds`` (crashed deliveries).

    Safe by construction: nothing in ``tmp/`` was ever linked into ``new/``,
    so no reader could have observed it. ``max_age_seconds`` exists only to
    avoid racing a delivery that is still mid-write in another process.
    """
    layout = ensure_layout(root)
    now = time.time()
    removed: list[Path] = []
    for entry in layout.tmp.iterdir():
        try:
            if now - entry.stat().st_mtime > max_age_seconds:
                entry.unlink()
                removed.append(entry)
        except FileNotFoundError:
            continue
    return removed


@contextmanager
def _lock(root: Path):
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (root / ".lock").open("a+b") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def deliver(root: Path, key: str, payload: bytes) -> DeliveryResult:
    """Serialize delivery and claim so a claimed key cannot be redelivered."""
    with _lock(root):
        return _deliver(root, key, payload)


def claim(root: Path, key: str) -> ClaimResult:
    """Claim a pending message while holding the mailbox lock."""
    with _lock(root):
        return _claim(root, key)
