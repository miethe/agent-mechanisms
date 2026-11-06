# Scan and validation report

A recursive case-insensitive `rg` scan of the complete staging tree checked home and volume path prefixes, identifiers, URL and IPv4 patterns, and sensitive context terms; it produced no matches. The eight files, including hidden-file inventory, tests, metadata and documentation, were inspected in context. Instruction-file fixtures are created at runtime; no prohibited instruction filenames or directories are committed. No usernames, absolute home or volume paths, hosts, IP addresses, internal identifiers, credentials, or private conversation quotations were found. No generated outputs or history are included in the export. This is a self-scan, not an independent third-party review; the author signed off on publication on 2026-11-06 after it was re-run on the final tree.

Fresh copy and empty home, Python 3.12.0 on Darwin; installed with pip using the environment's existing setuptools, without dependency downloads. Command (the temporary path is generated at runtime):

```sh
temp_root=$(mktemp -d /tmp/context-budget.XXXXXX)
cp -R release-staging/agent-mechanisms/agent-context-budget "$temp_root/package"
mkdir "$temp_root/home"
cd "$temp_root/package"
env -i HOME="$temp_root/home" PATH="$PATH" python3 -m venv --system-site-packages "$temp_root/venv"
env -i HOME="$temp_root/home" PATH="$PATH" "$temp_root/venv/bin/python" -m pip install --no-build-isolation --no-deps .
env -i HOME="$temp_root/home" PATH="$PATH" "$temp_root/venv/bin/python" -m pytest -q tests/test_cli.py
```

`3 passed in 0.36s`
