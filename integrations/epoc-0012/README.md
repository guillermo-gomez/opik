# EPOC-0012: Opik + Langfuse + Prometheus + Grafana

Development-only, synthetic E2E observability scaffold. This does not establish live ingestion into Opik or Langfuse.

Langfuse project: https://us.cloud.langfuse.com/project/cmv1xs63i02hyad0epdgtckcm/traces

## Design
- Opik: agent evaluation and tracing
- Langfuse: independent trace and token/cost comparison
- Prometheus: operational metrics, alert rules, time-series
- Grafana: unified operational dashboard
- Correlation: wp_id, run_id, agent_id, model_id, trace_id

## Local demonstration
```bash
cd integrations/epoc-0012
docker compose up -d --build
python -m unittest discover -s tests -v
```
Open Grafana at http://localhost:3000 (credentials provided locally through environment variables), Prometheus at http://localhost:9090 and metrics at http://localhost:8008/metrics.

Requires Docker Compose. This is an isolated synthetic metrics exporter, not a production Opik/Langfuse integration. Do not expose local services publicly. Change Grafana credentials before deployment. Prometheus labels must not include unique run_id or trace_id (cardinality risk); use trace logs for per-run details.

## E2E acceptance criteria
1. Synthetic run emits success/error and latency metrics; Prometheus scrapes them.
2. Grafana panels display throughput, errors, latency and estimated costs.
3. Identical real run IDs can be located in both Opik and Langfuse once credentials and SDK adapters are configured.
4. Independent comparisons identify missing spans, ingestion delay and mismatched tokens/costs.
5. CI tests and a documented security review pass before any deployment.

## Secrets
Do not commit API keys. For future live tests use OPIK_API_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY and LANGFUSE_BASE_URL=https://us.cloud.langfuse.com in a local secrets manager.
