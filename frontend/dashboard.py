import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Wi-Fi Threat Monitoring Console", layout="wide")

st.title("📡 Wi-Fi Threat Monitoring Console")
st.caption("WPA2 Deauthentication & Handshake Capture Detection")

DATA = Path(__file__).resolve().parents[1] / "data" / "timeline.csv"

if not DATA.exists():
    st.warning("Waiting for PCAP data...")
    st.stop()

df = pd.read_csv(DATA)

if df.empty:
    st.warning("No activity detected yet.")
    st.stop()

# --- Normalize timestamp ---
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
else:
    st.error(f"timeline.csv missing 'timestamp' column. Found columns: {list(df.columns)}")
    st.stop()

# --- Normalize column names across versions ---
# deauth_count could be 'count' in older versions
if "deauth_count" not in df.columns and "count" in df.columns:
    df = df.rename(columns={"count": "deauth_count"})

# rate could be stored under different names depending on backend version
if "deauth_rate" not in df.columns:
    if "rate" in df.columns:
        df = df.rename(columns={"rate": "deauth_rate"})
    elif "deauth_rate_per_min" in df.columns:
        df = df.rename(columns={"deauth_rate_per_min": "deauth_rate"})

# Final validation
required = ["deauth_count", "deauth_rate"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"timeline.csv missing columns: {missing}. Found columns: {list(df.columns)}")
    st.stop()

st.subheader("📈 Deauthentication Activity Timeline")
st.line_chart(df.set_index("timestamp")[["deauth_count", "deauth_rate"]])

st.subheader("🚨 Detected Events")
st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)

st.markdown("---")
st.markdown(
    "> **Did you know?** With less than ₹5,000 worth of hardware, attackers can exploit "
    "WPA2 networks by abusing unauthenticated deauthentication frames."
)
