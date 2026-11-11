# session-watcher-design

## Problem

Concurrent agent sessions can leave a message unread, a handoff stale, or work without an identified landing path.

## Mechanism

A census can derive conditions from session events and attach the observations that triggered them. Selected execution boundaries may also be enforced by guards.

## Shape

Use a read-only watcher with freshness checks and positive and negative controls. Expose fired, quiet, and unmeasured states to a named reader; define how observations clear after recovery.

## Failure modes

Missing or unreadable inputs must not be reported as quiet. False positives and stale observations can mislead a reader. A guard without a recovery path can block valid work.

## What we learned

Design each signal with a working producer, a reader, and a way to clear after recovery. This is a design proposal, not evidence that an entire topology was retired or that a watcher is currently operating.
