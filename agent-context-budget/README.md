# agent-context-budget

Use this tool when instruction files may exceed a harness's configured byte budget. It measures root and nested instruction chains, checks required root anchors within a byte prefix, and reports file totals and optional baseline deltas.

In a historical incident, a 79,553-byte instruction file was truncated at 32,768 bytes, leaving about 41% visible. This was observed with a particular CLI version and configuration; the limit is not universal. Set budgets from your own harness and configuration.

## Quick start

Requires Python 3.10 or later and pip; pytest is needed for tests. The runtime uses only Python's standard library. Installation uses setuptools. The commands below use a POSIX shell; Windows users can run equivalent commands in their shell. No particular harness version is required or detected.

```sh
python -m pip install .
mkdir -p example/nested
printf 'Required guidance.\n' > example/AGENTS.md
printf 'Nested guidance.\n' > example/nested/AGENTS.md
agent-context-budget example --cap 100 --root-cap 100 --prefix 32 --anchor 'Required guidance'
agent-context-budget example --cap 100 --root-cap 100 --prefix 32 --json > baseline.json
agent-context-budget example --cap 100 --root-cap 100 --prefix 32 --baseline baseline.json
```

The commands create synthetic example files locally. Exit 0 means all requested checks passed, 1 means a budget or anchor failed, and 2 means invalid arguments or unreadable input. Diagnostics go to stderr for input errors. JSON includes entries, total bytes, estimated tokens, chains, findings, and optionally delta_bytes. A baseline must be JSON with a nonnegative integer `total_bytes`; it is never created implicitly. Bytes divided by four are an estimate, not measured tokens or billing.

Discovery recursively reads regular files named by `--name` (default `AGENTS.md`) under the supplied root, including untracked files. Symlinked instruction files are excluded. The root file is required. Each chain is the root and discovered ancestor files through a nested file; no harness behavior, ordering, separators, ignore rules, configuration, dynamic injection, or other file names are inferred. An anchor must fit fully inside the root prefix. This is an inspection tool, not a security boundary or hook; it does not modify the target. Filesystem permissions are those of the invoking user; unreadable files cause an error where the OS reports one. No store or service is required. Inspect output before integrating it into a gate.

Uninstall with `python -m pip uninstall agent-context-budget`. Maintainer and security reporting contact: this repository's GitHub issues. For a security report, open an issue asking for a private channel and leave exploit details out of the public issue. See PROVENANCE.md for scope.

## Authors

Nick Miethe. Developed with Metis, Nick's AI collaborator.

Versions published before 2026-11-10 were released under the MIT License.
