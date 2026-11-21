# EPOC-0012 — Governance & execution architecture

Status: Proposed | Owner: Human Product Owner | Version: 0.1 | Scope: SAP ME-compatible synthetic pilot

## System of record
- Jira Cloud: epics, stories, tasks, bugs, sprint, priorities, dependencies, workflow and approvals.
- GitHub: code, ADRs, feature map, pull requests, test reports, immutable commit references.
- Opik + Langfuse: agent/model tracing and comparative evaluations.
- Prometheus + Grafana: numerical metrics, alerting and dashboards.
- AG-01 manages **what/who/when**, never technical choices; AG-02 owns **why/options/trade-offs**, never sprint status.
- Human PO approves high-impact architecture, security exceptions, production access, budgets and acceptance. Agents are logical identities, not nine Jira seats.

## Governance and execution (Mermaid)
```mermaid
flowchart TD
  PO["Human Product Owner"] --> J["Jira: backlog, sprints, releases"]
  J --> A1["AG-01 Flow Coordinator"]
  A1 -->|"ambiguous structural requirement"| A2["AG-02 ADR Architect"]
  A2 -->|"ADR proposed / decision gate"| PO
  PO -->|"accepted ADR"| A1
  A1 -->|"ready stories / dependencies"| ORCH["Work orchestrator"]
  ORCH --> WORKERS["AG-03..AG-06 implementation & simulation"]
  WORKERS --> PR["GitHub PR + Feature Map"]
  PR --> A7["AG-07 QA & Security gate"]
  WORKERS --> A8["AG-08 LLM Evals & tracing"]
  PR --> A9["AG-09 CI/CD & SRE"]
  A7 -->|"pass"| ACCEPT["Human Acceptance"]
  A7 -->|"fail"| WORKERS
  ACCEPT -->|"approved"| DONE["Jira Done"]
  A8 --> O["Opik / Langfuse"]
  A9 --> M["Prometheus / Grafana"]
  O --> A1
  M --> A1
  PR --> SYNC["Jira Sync: idempotent event bridge"]
  SYNC --> J
```

## Sequence: ambiguous requirement to Done
```mermaid
sequenceDiagram
  autonumber
  actor PO as Human PO
  participant J as Jira
  participant F as AG-01 Flow
  participant A as AG-02 ADR
  participant W as AG-03..06 Workers
  participant Q as AG-07 QA
  participant E as AG-08 Evals
  participant G as GitHub/CI
  participant S as Jira Sync
  PO->>J: Register requirement
  J->>F: Issue created/updated
  F->>F: Classify structural ambiguity
  alt Architecture decision required
    F->>A: Request ADR (issue ID, constraints)
    A->>G: Open ADR Proposed PR
    A->>PO: Alternatives, costs, risks, unanswered assumptions
    PO->>A: Accept or reject
    A->>G: Version accepted ADR
    A->>F: ADR ID and decision
  end
  F->>J: Set Ready only if DoR satisfied
  F->>W: Dispatch independent tasks
  par Implementation
    W->>G: Commit + PR
  and Agent evaluation
    W->>E: Trace + eval evidence
  end
  loop Bounded self-correction
    G->>Q: Tests, scans, contracts
    Q-->>W: Failures with evidence
    W->>G: Correct + rerun
  end
  Q-->>F: QA verdict and security veto
  alt All gates pass
    F->>PO: Human acceptance request
    PO->>J: Approve
    G->>S: PR/CI event
    S->>J: Transition Done with evidence
  else Failure or unresolved ADR
    F->>J: Blocked / In Progress with reason
  end
```

## Agent governance matrix
| ID | Agent | Owns | Artifact | Must not do |
|---|---|---|---|---|
| AG-01 | Scrum Master & Flow Coordinator | backlog, sprint, blockers, dependencies | Jira issue/sprint | choose architecture or bypass DoR |
| AG-02 | Enterprise & ADR Architect | alternatives, decisions, TOGAF, contracts | ADR in Git | manage sprint or self-accept high-impact ADR |
| AG-03 | SAP ME/MES Specialist | manufacturing semantics, routes, WIP | domain schemas | design numerical solver |
| AG-04 | Backend & Integration Engineer | API, persistence, service contracts | FastAPI/OpenAPI | override accepted ADR |
| AG-05 | Frontend & Visualization Engineer | UX, UI tests | views/feature map | embed business logic |
| AG-06 | Simulation & Optimization Engineer | SimPy/SciPy/Pyomo/Ipopt/OpenModelica | solver artifacts | invent SAP semantics |
| AG-07 | QA & Security Auditor | independent test/security gates | verdicts, risk reports | approve own failing build |
| AG-08 | LLM Evaluation & Observability | model eval, cost, traces | Opik/Langfuse datasets | replace deterministic engineering checks |
| AG-09 | DevOps & SRE | CI, Docker, Prometheus/Grafana | pipelines, dashboards | deploy without QA and authorization |

## ADR trigger rule
AG-01 flags: new persistent data model, contract breaking change, solver strategy, security boundary, cloud vs local, observability provider, irreversible migration, cost above approved budget. AG-02 checks existing accepted ADRs and proposes a superseding ADR if needed. Missing evidence => unresolved question, not guessed answer.

## Security boundaries
- Only Jira Sync holds Jira write credentials; agents submit structured events to it.
- AG-07 can block release; only human can override via documented, time-bounded exception.
- GitHub PR checks are not equivalent to human acceptance.
- No SAP production access; no untrusted MCP shell/file/network execution.
- No Jira API, Opik, Langfuse or other secret in code or traces.
