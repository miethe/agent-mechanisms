from concurrent.futures import ThreadPoolExecutor

import pytest
from local_maildir import claim, deliver, list_pending, read


def test_delivery_claim_and_duplicate(tmp_path):
    assert deliver(tmp_path, "message", b"hello").delivered
    assert not deliver(tmp_path, "message", b"other").delivered
    assert list_pending(tmp_path) == ["message"]
    result = claim(tmp_path, "message")
    assert result.claimed and read(result.path) == b"hello"
    assert not claim(tmp_path, "message").claimed
    assert not deliver(tmp_path, "message", b"other").delivered


def test_concurrent_claims_have_one_winner(tmp_path):
    deliver(tmp_path, "message", b"hello")
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda _: claim(tmp_path, "message"), range(16)))
    assert sum(result.claimed for result in results) == 1


def test_unsafe_key_rejected(tmp_path):
    with pytest.raises(ValueError):
        deliver(tmp_path, "../message", b"x")


def test_claim_races_duplicate_delivery(tmp_path):
    deliver(tmp_path, "message", b"original")
    with ThreadPoolExecutor(max_workers=2) as pool:
        pending = [pool.submit(claim, tmp_path, "message"),
                   pool.submit(deliver, tmp_path, "message", b"duplicate")]
        claimed, duplicate = [future.result() for future in pending]
    assert claimed.claimed
    assert not duplicate.delivered
    assert list_pending(tmp_path) == []
    assert read(claimed.path) == b"original"


def test_short_writes_are_retried(tmp_path, monkeypatch):
    import local_maildir
    original = local_maildir.os.write
    monkeypatch.setattr(local_maildir.os, "write", lambda fd, data: original(fd, data[:2]))
    result = deliver(tmp_path, "message", b"abcdef")
    assert read(result.path) == b"abcdef"
