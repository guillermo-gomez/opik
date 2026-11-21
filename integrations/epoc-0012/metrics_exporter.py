"""Synthetic-only metrics exporter for EPOC-0012 observability smoke tests."""
import os
import time
from prometheus_client import Counter, Histogram, Gauge, start_http_server

RUNS = Counter("epoc_wp_runs_total", "WP runs", ["engine", "status"])
DURATION = Histogram("epoc_wp_duration_seconds", "WP run duration", ["engine"],
                     buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10, 30, 60, float("inf")))
COST = Counter("epoc_llm_estimated_cost_usd_total", "Estimated model cost", ["model"])
ACTIVE = Gauge("epoc_active_workers", "Active workers", ["engine"])

def synthetic_tick():
    engine = "synthetic_scipy"
    ACTIVE.labels(engine).set(1)
    started = time.monotonic()
    time.sleep(0.02)
    DURATION.labels(engine).observe(time.monotonic() - started)
    RUNS.labels(engine, "success").inc()
    COST.labels("mock-model").inc(0.0001)
    ACTIVE.labels(engine).set(0)

if __name__ == "__main__":
    start_http_server(int(os.getenv("METRICS_PORT", "8008")))
    while True:
        synthetic_tick()
        time.sleep(5)
