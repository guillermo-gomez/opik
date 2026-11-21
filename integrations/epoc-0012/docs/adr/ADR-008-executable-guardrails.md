# ADR-008 — Executable boundaries, single writer and exception governance
Status: Proposed | Owner: AG-02 | Human acceptance: Pending | Jira: TBD

## Context
Instructions alone cannot stop agents from crossing architecture boundaries, changing shared roots or inventing APIs.

## Alternatives
A. Written conventions only: low cost, no mechanical enforcement.
B. Feature-owned folders and contracts, automated dependency checks, protected PR and narrowly approved exceptions.
C. Full custom static/runtime analysis of all languages: strongest coverage, high cost.

## Proposed decision
Adopt B initially, then extend coverage. Five invariants: conventional path is easier than shortcut; forbidden dependencies fail mechanically; each durable value has exactly one writer; new features add isolated files rather than switches in shared roots; exceptions are narrow, explicit, time-limited, reviewed architectural changes.

## Feature cards
Each feature owns `feature.json`, `entrypoints.json`, `contracts.json`, `owner.json`, `exceptions.json`. They declare the semantic ID, entrypoints, API/events, durable writes and exception references. These are EPOC-0012-defined cards.

## Consequences
Required CI architecture checks, negative tests, contract versioning, no direct-to-main pushes, approved ADR for exceptions. Python AST checks are only an initial approximation; dynamic imports, reflection, non-Python dependencies and side effects require stronger analysis. Agent self-approval forbidden.
