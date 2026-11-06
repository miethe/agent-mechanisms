"""Measure explicitly selected instruction files and nested chains in bytes."""
import argparse
import json
import sys
from pathlib import Path


def inspect(root, name, cap, root_cap, prefix, anchors):
    root = Path(root).resolve(strict=True)
    if not root.is_dir() or not name or Path(name).name != name or name in ('.', '..'):
        raise ValueError('root must be a directory and name must be a filename')
    if min(cap, root_cap, prefix) < 0 or any(not a for a in anchors):
        raise ValueError('budgets must be nonnegative and anchors must be nonempty')
    root_file = root / name
    if not root_file.is_file() or root_file.is_symlink():
        raise ValueError('root instruction file missing or not a regular file')
    files = sorted(p for p in root.rglob(name) if p.is_file() and not p.is_symlink())
    data = {p: p.read_bytes() for p in files}
    root_data = data[root_file]
    findings = []
    if len(root_data) > root_cap:
        findings.append(f'{name}: {len(root_data)} bytes exceeds root cap {root_cap}')
    for anchor in anchors:
        needle = anchor.encode('utf-8')
        offset = root_data.find(needle)
        if offset < 0 or offset + len(needle) > prefix:
            findings.append(f'{name}: anchor {anchor!r} missing from first {prefix} bytes')
    chains = []
    for path in files:
        chain = [p for p in files if p.parent == path.parent or p.parent in path.parent.parents]
        size = sum(len(data[p]) for p in chain)
        chains.append({'file': str(path.relative_to(root)), 'bytes': size})
        if size > cap:
            findings.append(f'{path.relative_to(root)}: chain {size} bytes exceeds cap {cap}')
    entries = [{'file': str(p.relative_to(root)), 'bytes': len(data[p])} for p in files]
    return {'entries': entries, 'total_bytes': sum(e['bytes'] for e in entries),
            'estimated_tokens': sum(e['bytes'] for e in entries) // 4,
            'chains': chains, 'findings': findings}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--name', default='AGENTS.md')
    parser.add_argument('--cap', type=int, required=True)
    parser.add_argument('--root-cap', type=int, required=True)
    parser.add_argument('--prefix', type=int, required=True)
    parser.add_argument('--anchor', action='append', default=[])
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--baseline', type=Path)
    args = parser.parse_args(argv)
    try:
        report = inspect(args.root, args.name, args.cap, args.root_cap, args.prefix, args.anchor)
        if args.baseline:
            baseline = json.loads(args.baseline.read_text(encoding='utf-8'))
            value = baseline['total_bytes']
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError('baseline total_bytes must be a nonnegative integer')
            report['delta_bytes'] = report['total_bytes'] - value
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for entry in report['entries']:
            print(f"{entry['file']}: {entry['bytes']} bytes")
        print(f"total: {report['total_bytes']} bytes; estimated tokens: {report['estimated_tokens']}")
        if 'delta_bytes' in report:
            print(f"baseline delta: {report['delta_bytes']:+d} bytes")
        for finding in report['findings']:
            print(f'FAIL: {finding}')
    return 1 if report['findings'] else 0


if __name__ == '__main__':
    sys.exit(main())
