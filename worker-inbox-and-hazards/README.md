# Worker inbox and hazards

A local inbox claims each pending message once across cooperating consumers, using the included mailbox primitives. A hazard helper selects the latest event per key, matches active patterns against work text, and requires separate fix and validation evidence for transitions. Callers must persist their own hazard events; this extraction is a library, not a daemon or a complete event store.

Requires a local filesystem with POSIX advisory locks and hard links. All writers must use the mailbox library. Claims and downstream effects are not transactional; directory entries are not fsynced. Run tests with `python -m pytest -q`.
