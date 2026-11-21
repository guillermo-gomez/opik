# ADR-007 — Semantic domain repositories and per-feature branches
Status: Proposed | Owner: AG-02 | Human acceptance: Pending | Jira: TBD

## Context
A coding agent tends to edit nearby code and reuse local patterns, even when domain boundaries would be violated. EPOC-0012 needs isolated ownership, testability and semantic versioning.

## Options and trade-offs
1. Single monorepo with modular features: simpler CI, weaker deployment boundaries.
2. Domain-oriented repositories with per-feature branches: clear ownership and independent releases, additional cross-repo contracts and CI overhead.
3. One repository per small function: extreme isolation but high coordination and duplication cost.

## Proposed decision
Choose 2 for independently deployable domains, not every method. Target repositories (not yet created): epoc12-agent-orchestrator, epoc12-mes-simulator, epoc12-solver-engine, epoc12-observability, epoc12-governance. Every feature uses a short-lived branch linked to a verified Jira issue key and a scoped PR. Do not reorganize the upstream Opik fork destructively.

## Consequences
Versioned interfaces, consumer-driven contract tests, cross-repo integration manifests, CODEOWNERS, required CI, independent AG-07 review and AG-02 approval for boundary changes. No repositories claimed created.
