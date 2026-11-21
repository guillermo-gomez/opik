# EPOC-0012 — StateChart maestro y control de entrega
Status: Proposed | Jira Cloud: not connected | Product Owner approval: publication authorized once, architectural acceptance pending

## Systems of record
Jira: epics, stories, WP mapping, sprint, status and acceptance. GitHub: ADR, code, PR, tests and evidence. Opik and Langfuse: model/agent traces. Prometheus and Grafana: operational metrics and dashboards. Never claim a synthetic test is a live Jira/LLM integration.

## Program At-a-Glance
```mermaid
flowchart TB
 P["EPOC-0012"] --> G["Governance / Jira / AG-01"]
 P --> A["Architecture / ADR / AG-02"]
 P --> W["Engineering AG-03..06"]
 P --> Q["QA AG-07 / Evals AG-08"]
 P --> O["SRE AG-09 / Observability"]
 G --> B["Baseline: 15 epics / 166 stories / 96 WPs (not imported)"]
 G --> S["Scrum + Kanban / 25 installation tasks"]
 A --> D["ADR Proposed → Accepted → Superseded"]
 A --> C["Contracts / Single Writer / Dependency policy"]
 W --> M["MES semantics / APIs / UI / Solvers"]
 Q --> T["Tests / Skills / Guardrails"]
 O --> X["Opik + Langfuse / Prometheus + Grafana"]
 D --> R{"Architecture gate"}
 C --> R
 R -->|Accepted| M
 R -->|Pending| D
 M --> PR["GitHub PR + CI"]
 PR --> T
 T -->|Fail| M
 T -->|Pass| H["Human acceptance"]
 H -->|Approved| DONE["Jira Done"]
```

## Story lifecycle
```mermaid
stateDiagram-v2
 [*] --> Intake
 Intake --> Classified
 Classified --> ArchitectureReview: structural ambiguity
 ArchitectureReview --> ADRProposed
 ADRProposed --> ADRReview
 ADRReview --> ADRProposed: revise
 ADRReview --> Ready: accepted ADR and DoR
 Classified --> Ready: no ADR needed, DoR pass
 Ready --> SprintCommitted
 SprintCommitted --> InProgress
 InProgress --> CodeReview: PR and tests
 CodeReview --> InProgress: changes requested
 CodeReview --> AutomatedQA: review pass
 AutomatedQA --> InProgress: tests or eval fail
 AutomatedQA --> SecurityBlocked: critical security veto
 AutomatedQA --> HumanAcceptance: all mandatory gates pass
 SecurityBlocked --> InProgress: independently resolved
 HumanAcceptance --> InProgress: rejected
 HumanAcceptance --> Done: explicit human approval
 Done --> [*]
```

## Decision and implementation sequence
```mermaid
sequenceDiagram
 autonumber
 actor PO as Human PO
 participant J as Jira
 participant F as AG-01 Flow
 participant A as AG-02 ADR
 participant W as AG-03..06
 participant C as GitHub CI
 participant Q as AG-07 QA
 participant E as AG-08 Evals
 participant S as Jira Sync
 PO->>J: Submit requirement
 J->>F: Intake event
 F->>F: Classify, dependency check, DoR
 alt Architectural ambiguity
 F->>A: Request ADR, freeze premature decomposition
 A->>A: Compare accepted ADRs, options and trade-offs
 A->>C: ADR Proposed PR
 A->>PO: Request high-impact approval
 PO-->>A: Accept / revise
 A-->>F: Accepted ADR ID or blocker
 end
 F->>W: Dispatch isolated WP
 loop Bounded self-correction
 W->>C: Commit and PR
 C->>Q: Deterministic checks and security scans
 C->>E: Agent eval evidence
 Q-->>W: Defects, if any
 E-->>W: Score and corrections, if any
 end
 Q-->>F: Independent gate verdict
 F->>PO: Acceptance bundle
 PO->>J: Approve / reject
 C->>S: Signed CI event with Jira issue and WP
 S->>J: Idempotent evidence update, no bypass of approval
```

## Agent behavior
AG-01 owns what/who/when; AG-02 owns why/trade-offs; AG-03 MES; AG-04 backend; AG-05 frontend; AG-06 solvers; AG-07 QA/security veto; AG-08 LLM evaluation; AG-09 DevOps/SRE. Nine logical identities share one authorized integration identity, not nine Jira accounts.

### Engineering correction loop
```mermaid
flowchart LR
 F["Feature Map + Story"] --> I["Implement"]
 I --> T["Deterministic test"]
 T --> P{"Pass?"}
 P -->|No| C["Diagnose and correct"]
 C --> I
 P -->|Yes| R["Independent review / QA"]
 R --> H["Human acceptance"]
```
### Skill improvement loop
```mermaid
flowchart LR
 S["Versioned skill"] --> A["Parallel agent trials"]
 A --> E["Independent held-out evaluation"]
 E --> G{"Score >=90 and no critical failure?"}
 G -->|No| R["Skill revision PR + regression"]
 R --> S
 G -->|Yes| P["Pin skill version"]
```
### Hard guardrails
```mermaid
flowchart LR
 S["Skill guidance"] --> A["Proposed action"]
 A --> P{"Deny-by-default policy"}
 P -->|Allow| T["Restricted tool / MCP"]
 P -->|Deny| B["Block + audit + Jira incident"]
 T --> Q["CI and QA"]
```
No agent may alter its own safety policy, test oracle or approval evidence to obtain a passing score.

## Verification and release
```mermaid
flowchart TD
 PR["PR"] --> PRE["Preproduction: unit, functional, component, fuzz, property, formal where feasible, static, mutation, coverage, benchmark, contract, lint, acceptance, regression, smoke, usability, UI/UX, penetration, threat model, performance"]
 PRE --> G1{"Required gates pass?"}
 G1 -->|No| FIX["Correct and retest"]
 FIX --> PRE
 G1 -->|Yes| DEP["Deploy: integration, TAP compare protocol TBD, load, shadow, config, soak"]
 DEP --> G2{"Staging gate"}
 G2 -->|No| RB["Rollback"]
 G2 -->|Yes| HA["Human release approval"]
 HA --> REL["Canary, monitoring, traffic shaping, flags, exceptions"]
 REL --> PROD["Authorized production"]
 PROD --> POST["Teeing, profiling, logs, chaos, monitoring, A/B, tracing, exploration, RUM, auditing, on-call"]
 POST -->|SLO breach| RB
```
This is a control taxonomy; listed tests are not necessarily implemented.

## Jira installation checklist (all unverified until Jira connection)
INS-001 branch status; 002 Docker/WSL/Compose; 003 Python tests; 004 monitoring stack; 005 Jira site; 006 EPOC12 project; 007 Scrum/Kanban boards; 008 issue types; 009 agent/WP/run/evidence fields; 010 GitHub integration; 011 15 epics; 012 166 stories; 013 96 WP links; 014 Sprint 0; 015 DoR/DoD; 016 REST/MCP auth; 017 9 logical identities; 018 idempotent Jira Sync; 019 CI status mapping; 020 E2E issue/PR/test/Jira; 021 Opik/Langfuse trace correlation; 022 Prometheus Jira metrics; 023 Grafana delivery dashboard; 024 security/cost/alerts; 025 retrospective.

## Dashboard contract
Show real Jira counts by status, sprint, epic, WP, blocked dependencies, ADR state, agent score/retries, CI failures, QA veto, latency p95, errors, token costs and SLOs. Mark unavailable integrations as NOT CONNECTED; do not display planned counts as completed.
