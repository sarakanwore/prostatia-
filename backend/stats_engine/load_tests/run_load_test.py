"""Script de test de charge (Load Testing) automatisé pour le STATIA Stats Engine.

Ce script simule des requêtes concurrentes massives à travers la pile ASGI FastAPI
et mesure :
- Le débit (requêtes par seconde)
- Les temps de réponse (min, moyenne, p50, p90, p95, p99, max)
- Le taux de succès et les erreurs éventuelles
"""

import asyncio
import time
import statistics
from typing import List, Dict, Any
import httpx
import numpy as np

from app.main import app


async def send_worker(
    client: httpx.AsyncClient,
    tasks_queue: asyncio.Queue,
    results: List[Dict[str, Any]],
):
    while not tasks_queue.empty():
        req_type, path, payload = await tasks_queue.get()
        start = time.perf_counter()
        try:
            if req_type == "GET":
                response = await client.get(path)
            else:
                response = await client.post(path, json=payload)
            elapsed_ms = (time.perf_counter() - start) * 1000
            results.append({
                "status_code": response.status_code,
                "elapsed_ms": elapsed_ms,
                "success": response.status_code == 200,
                "path": path,
            })
        except Exception as e:
            elapsed_ms = (time.perf_counter() - start) * 1000
            results.append({
                "status_code": 0,
                "elapsed_ms": elapsed_ms,
                "success": False,
                "error": str(e),
                "path": path,
            })
        finally:
            tasks_queue.task_done()


async def run_load_test(total_requests: int = 300, concurrency: int = 20):
    print(f"\n{'='*65}")
    print(f" Démarrage du Test de Charge – PROSTATIA Stats Engine")
    print(f" Total requêtes : {total_requests} | Concurrence (workers) : {concurrency}")
    print(f"{'='*65}\n")

    # Scénarios de tests représentatifs
    scenarios = [
        ("GET", "/health", None),
        ("GET", "/api/v1/methods", None),
        ("GET", "/api/v1/methods/t_test_independent", None),
        ("POST", "/api/v1/execute", {
            "method_id": "summary_statistics",
            "data_payload": {"data": np.random.normal(10, 2, 50).tolist()},
        }),
        ("POST", "/api/v1/execute", {
            "method_id": "t_test_independent",
            "data_payload": {
                "group_a": np.random.normal(10, 2, 40).tolist(),
                "group_b": np.random.normal(12, 2, 40).tolist(),
            },
        }),
        ("POST", "/api/v1/execute", {
            "method_id": "normal_distribution",
            "data_payload": {"mu": 0.0, "sigma": 1.0, "x": 1.96, "query_type": "cdf"},
        }),
    ]

    queue = asyncio.Queue()
    for i in range(total_requests):
        scenario = scenarios[i % len(scenarios)]
        queue.put_nowait(scenario)

    transport = httpx.ASGITransport(app=app)
    results: List[Dict[str, Any]] = []

    start_total = time.perf_counter()
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        workers = [
            asyncio.create_task(send_worker(client, queue, results))
            for _ in range(concurrency)
        ]
        await queue.join()
        for w in workers:
            w.cancel()

    total_duration = time.perf_counter() - start_total
    latencies = [r["elapsed_ms"] for r in results]
    successes = sum(1 for r in results if r["success"])
    failures = len(results) - successes

    latencies.sort()
    p50 = statistics.median(latencies)
    p90 = latencies[int(len(latencies) * 0.90)]
    p95 = latencies[int(len(latencies) * 0.95)]
    p99 = latencies[int(len(latencies) * 0.99)]

    print(f"--- RÉSULTATS DU TEST DE CHARGE ---")
    print(f"Durée totale d'exécution : {total_duration:.2f} s")
    print(f"Débit moyen (Throughput) : {len(results) / total_duration:.1f} req/s")
    print(f"Succès                   : {successes} / {len(results)} ({successes/len(results)*100:.1f}%)")
    print(f"Échecs                   : {failures}")
    print(f"Latence moyenne          : {statistics.mean(latencies):.2f} ms")
    print(f"Latence Min              : {min(latencies):.2f} ms")
    print(f"Latence Médiane (p50)    : {p50:.2f} ms")
    print(f"Latence p90              : {p90:.2f} ms")
    print(f"Latence p95              : {p95:.2f} ms")
    print(f"Latence p99              : {p99:.2f} ms")
    print(f"Latence Max              : {max(latencies):.2f} ms")
    print(f"{'='*65}\n")

    assert failures == 0, f"Erreurs détectées lors du test de charge: {failures} échecs"
    assert p95 < 500, f"Latence p95 trop élevée: {p95:.2f}ms >= 500ms"
    print(">>> VALIDATION TEST DE CHARGE: SUCCÈS (100% de succès, SLA de latence respecté) <<<\n")


if __name__ == "__main__":
    asyncio.run(run_load_test(total_requests=300, concurrency=20))
