# Small hook pack

Two reusable text primitives: detect newly added handoff links in an index, counting duplicates while allowing wording changes; and remove quoted or fenced content before applying a separate text classifier. The latter is a heuristic, not a Markdown parser or decision detector. Neither primitive integrates with an agent runtime on its own.

Run `python src/small_hooks.py old.md new.md` to flag added links. Exit 1 means additions; exit 0 means none. Run tests with `python -m pytest -q`.
