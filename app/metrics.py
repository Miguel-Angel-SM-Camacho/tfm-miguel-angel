from prometheus_client import Counter, Gauge, Histogram

MODEL_LOADED = Gauge("model_loaded", "1 si el motor está cargado")
PREDICTIONS = Counter("predictions", "Recomendaciones atendidas", ["tipo"])           # -> predictions_total
PREDICTIONS_FAILED = Counter("predictions_failed", "Recomendaciones fallidas", ["tipo"])  # -> predictions_failed_total
LATENCY = Histogram("prediction_latency_seconds", "Latencia del motor", ["tipo"],
                    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10))
LAST_RISK = Gauge("last_risk_level_numeric", "Último nivel de riesgo (1 bajo, 2 moderado, 3 alto)")

# Crea las series a 0 desde el arranque, para que el panel de errores no salga vacío
for t in ("hard", "soft"):
    PREDICTIONS.labels(t)
    PREDICTIONS_FAILED.labels(t)