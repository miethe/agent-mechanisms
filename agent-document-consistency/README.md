# Agent document consistency

Compare named facts in a canonical document against a mirror. A caller supplies a regular expression containing a named `fact` group; each capture in the canonical document must appear in the mirror unless explicitly allowed. `stale` also reports line numbers of claims outside an accepted set. This checks selected facts, not semantic equivalence.

Run `python src/document_consistency.py canonical.md mirror.md --pattern '^Rule: (?P<fact>.+)$'`. Repeat `--allow VALUE` for intentional omissions. Exit status is 1 on missing facts, 0 otherwise. Run tests with `python -m pytest -q`.
