"""
ml_model.py
------------
Isolation Forest based anomaly detection.
Learns normal Wi-Fi behavior over time.
"""

from sklearn.ensemble import IsolationForest
import numpy as np

MODEL = None


def get_model():
    global MODEL
    if MODEL is None:
        MODEL = IsolationForest(
            n_estimators=100,
            contamination=0.1,
            random_state=42
        )
        # Initial dummy fit so model is usable immediately
        MODEL.fit([[0, 0]])
    return MODEL


def score_anomaly(model, features: dict) -> float:
    vector = [
        features["deauth_count"],
        features["deauth_rate_per_min"]
    ]
    return model.decision_function([vector])[0]
