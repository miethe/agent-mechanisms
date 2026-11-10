"""Compare declared document facts and report stale values."""
import argparse
import re
from pathlib import Path


def facts(text, pattern):
    """Return named ``fact`` captures; reject patterns without that group."""
    regex = re.compile(pattern, re.MULTILINE)
    if 'fact' not in regex.groupindex:
        raise ValueError('pattern needs a named fact group')
    return {match.group('fact').strip() for match in regex.finditer(text)}


def missing(canonical, mirror, pattern, allowed=()):
    return sorted(facts(canonical, pattern) - facts(mirror, pattern) - set(allowed))


def stale(text, pattern, accepted):
    regex = re.compile(pattern, re.MULTILINE)
    if 'fact' not in regex.groupindex:
        raise ValueError('pattern needs a named fact group')
    return [(text.count('\n', 0, m.start()) + 1, m.group('fact').strip())
            for m in regex.finditer(text) if m.group('fact').strip() not in accepted]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('canonical', type=Path)
    parser.add_argument('mirror', type=Path)
    parser.add_argument('--pattern', required=True, help='regex with named fact group')
    parser.add_argument('--allow', action='append', default=[])
    args = parser.parse_args(argv)
    omissions = missing(args.canonical.read_text(), args.mirror.read_text(), args.pattern, args.allow)
    for fact in omissions:
        print(f'missing: {fact}')
    return bool(omissions)


if __name__ == '__main__':
    raise SystemExit(main())
