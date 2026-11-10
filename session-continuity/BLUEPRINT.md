# session-continuity

## Problem

A long-running agent session may lose actionable context when its working context is compacted.

## Mechanism

Bind a session to a living handoff and append a small pointer-only seam at a compaction event. Record the outcome of each attempted write.

## Shape

A hook resolves a declared binding, updates an existing handoff atomically, and emits a receipt; the next session reads the handoff and verifies current state.

## Failure modes

A missing binding, stale cursor, missing destination, concurrent write, or failed hook can silently prevent a handoff. Treat a receipt as an observation rather than proof of successful rehydration.

## What we learned

Fail-open enrichment still needs observable outcomes. Count actual producer events and distinguish no destination from a successful write.

