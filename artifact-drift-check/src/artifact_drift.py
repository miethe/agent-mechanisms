"""Compare an upstream file or directory with its deployed copy."""
import argparse
from pathlib import Path


def compare(upstream, deployed):
    upstream, deployed = Path(upstream), Path(deployed)
    if not upstream.exists():
        return ['missing upstream']
    if not deployed.exists():
        return ['missing deployment']
    if upstream.is_file() and deployed.is_file():
        return [] if upstream.read_bytes() == deployed.read_bytes() else ['differs: .']
    if not upstream.is_dir() or not deployed.is_dir():
        return ['type mismatch: .']
    def entries(root):
        return {p.relative_to(root).as_posix(): p for p in root.rglob('*')}
    a, b = entries(upstream), entries(deployed)
    findings = []
    for name in sorted(a.keys() | b.keys()):
        if name not in a:
            findings.append(f'only in deployment: {name}')
        elif name not in b:
            findings.append(f'only in upstream: {name}')
        elif a[name].is_dir() != b[name].is_dir():
            findings.append(f'type mismatch: {name}')
        elif a[name].is_file() and a[name].read_bytes() != b[name].read_bytes():
            findings.append(f'differs: {name}')
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('upstream', type=Path)
    parser.add_argument('deployed', type=Path)
    args = parser.parse_args(argv)
    findings = compare(args.upstream, args.deployed)
    for finding in findings:
        print(finding)
    return bool(findings)


if __name__ == '__main__':
    raise SystemExit(main())
