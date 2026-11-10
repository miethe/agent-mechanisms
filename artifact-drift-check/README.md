# Artifact drift check

Compare a source file or directory with a deployed copy. Missing sides, extra paths, type mismatches and differing file bytes are reported deterministically; no changes are made. Symbolic links are followed by Python's filesystem APIs, so compare trusted trees only. Unlike the original checker, this small extraction does not infer history or exempt generated regions.

Run `python src/artifact_drift.py upstream deployed`; it exits 1 for findings and 0 for equal trees. Run tests with `python -m pytest -q`.
