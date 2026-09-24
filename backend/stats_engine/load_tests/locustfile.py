from locust import HttpUser, task, between
import numpy as np


class StatsEngineUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def health_check(self):
        """Vérifie l'état de santé du service."""
        self.client.get("/health")

    @task(3)
    def list_methods(self):
        """Consulte le catalogue complet des méthodes."""
        self.client.get("/api/v1/methods")

    @task(2)
    def get_method_details(self):
        """Consulte la fiche d'une méthode spécifique."""
        self.client.get("/api/v1/methods/t_test_independent")

    @task(4)
    def execute_summary_stats(self):
        """Exécute un calcul de statistiques descriptives univariées."""
        data = np.random.normal(loc=10, scale=2, size=100).tolist()
        payload = {
            "method_id": "summary_statistics",
            "data_payload": {"data": data},
        }
        self.client.post("/api/v1/execute", json=payload)

    @task(3)
    def execute_t_test(self):
        """Exécute un test t de Student avec vérification d'hypothèses."""
        group_a = np.random.normal(loc=12, scale=3, size=50).tolist()
        group_b = np.random.normal(loc=10, scale=3, size=50).tolist()
        payload = {
            "method_id": "t_test_independent",
            "data_payload": {
                "group_a": group_a,
                "group_b": group_b,
            },
        }
        self.client.post("/api/v1/execute", json=payload)

    @task(2)
    def execute_probability_law(self):
        """Évalue une loi de probabilité (normale)."""
        payload = {
            "method_id": "normal_distribution",
            "data_payload": {
                "mu": 0.0,
                "sigma": 1.0,
                "x": 1.96,
                "query_type": "cdf",
            },
        }
        self.client.post("/api/v1/execute", json=payload)

