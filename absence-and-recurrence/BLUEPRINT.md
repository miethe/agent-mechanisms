# absence-and-recurrence

## Problem

An expected artifact can disappear while a recurring hazard remains unnoticed.

## Mechanism

Keep a ledger of expected artifacts and probe their presence and content digest. Record repeated hazards separately with evidence and timestamps.

## Shape

A read-only scheduled probe emits structured observations; a separate consumer reviews changes and decides whether restoration is appropriate. Exclude sensitive paths before any filesystem access.

## Failure modes

A missing ledger, unreadable path, stale probe, or inaccessible storage must be reported as unknown rather than healthy. Avoid restoring automatically from an unverified candidate.

## What we learned

A watcher needs a named reader and a positive control. A quiet result alone does not prove the probe ran.

