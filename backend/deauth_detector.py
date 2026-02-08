"""
deauth_detector.py

Rule-based detection using count + burst rate.
"""

def detect_deauth(features):
    count = features["deauth_count"]
    rate = features["deauth_rate_per_min"]
    burst = features["burst_score"]

    if count >= 30 and rate >= 20:
        return "HIGH"

    if count >= 15 and rate >= 10:
        return "MEDIUM"

    return "LOW"
