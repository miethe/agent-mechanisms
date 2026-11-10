# execution-boundaries

## Problem

Concurrent work and delegated execution can operate on stale state, ambiguous scope, or unverified outputs.

## Mechanism

Pin reads to a revision, identify the authorized scope before mutation, and verify outputs and actual resource use at the receiving boundary.

## Shape

Separate policy decisions from enforcement. Use a scoped launcher, a mutation guard, and a receiver that validates the result against the original assignment.

## Failure modes

A stale revision, ambiguous ownership, overbroad staging, missing artifact, or self-reported resource use can undermine the boundary. Failures must be visible and recovery paths explicit.

## What we learned

Rules are more reliable when the boundary is mechanically checked and the observed result is verified by an independent reader. Enforcement requires local policy and usability review.

