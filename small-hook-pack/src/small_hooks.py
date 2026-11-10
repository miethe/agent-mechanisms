"""Small, composable text checks suitable for use by a hook wrapper."""
import argparse
import re
from collections import Counter
from pathlib import Path

LINK = re.compile(r'\]\(\s*(?:\./)?handoff-([^\s)]+)\.md\s*\)|\[\[\s*handoff-([^\]]+)\]\]')


def links(text):
    return [next(group for group in match.groups() if group is not None) for match in LINK.finditer(text)]


def added_handoffs(old, new):
    counts = Counter(links(old))
    added = []
    for name in links(new):
        if counts[name]:
            counts[name] -= 1
        else:
            added.append(name)
    return added


def unquoted_text(text):
    text = re.sub(r'```.*?```|~~~.*?~~~', ' ', text, flags=re.S)
    text = re.sub(r'`[^`]*`|"[^"\n]*"|“[^”]*”', ' ', text)
    return '\n'.join(line for line in text.splitlines() if not line.lstrip().startswith('>'))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('old', type=Path)
    parser.add_argument('new', type=Path)
    args = parser.parse_args(argv)
    added = added_handoffs(args.old.read_text(), args.new.read_text())
    for name in added:
        print(f'new handoff link: {name}')
    return bool(added)


if __name__ == '__main__':
    raise SystemExit(main())
