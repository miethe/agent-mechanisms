# Agent mechanisms

Focused tools and blueprints for agent workflows.

- [agent-context-budget](agent-context-budget/) — Working code: measures instruction budgets; estimates tokens, not harness reads.
- [agent-document-consistency](agent-document-consistency/) — Working code: compares selected regex captures, not semantic equivalence.
- [artifact-drift-check](artifact-drift-check/) — Working code: compares files; symlinks require trust; history and exemptions are not inferred.
- [small-hook-pack](small-hook-pack/) — Working code: detects handoff links and filters text heuristically; no runtime integration.
- [local-maildir](local-maildir/) — Working code: experimental local mailbox; requires cooperating writers, POSIX locks and hard links; no power-loss or downstream transaction guarantee.
- [worker-inbox-and-hazards](worker-inbox-and-hazards/) — Working code: local inbox and hazard helpers; callers persist events; effects are nontransactional and directories are not fsynced.
- [absence-and-recurrence](absence-and-recurrence/) — Blueprint: monitors absence and recurring hazards; probes need a reader, positive controls and unknown states.
- [session-continuity](session-continuity/) — Blueprint: pointer handoffs across compaction; receipts do not prove rehydration.
- [execution-boundaries](execution-boundaries/) — Blueprint: scoped execution and result checks; enforcement requires local policy and usability review.
- [session-watcher-design](session-watcher-design/) — Blueprint: read-only watcher with fired, quiet and unmeasured states; does not show a watcher is operating.

## License

Apache-2.0; see [LICENSE](LICENSE) and [NOTICE](NOTICE).

## Tests

In each code folder, run `python3 -m pytest -q -p no:cacheprovider`.
