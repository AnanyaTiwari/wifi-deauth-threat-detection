import os
import pandas as pd
import streamlit as st

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Wi-Fi Threat Monitoring Console",
    layout="wide"
)

DATA_PATH = "../data/timeline.csv"

# ---------------- HEADER ----------------
st.title("📡 Wi-Fi Threat Monitoring Console")
st.caption("Deauthentication & Handshake Capture Detection (WPA2)")

st.markdown(
    """
This dashboard visualizes **Wi-Fi deauthentication activity**, a common attack
used to exploit **WPA2 protocol weaknesses** and capture handshakes
(e.g., Pwnagotchi-style attacks).
"""
)

st.markdown("---")

# ---------------- DATA LOADING ----------------
if not os.path.exists(DATA_PATH):
    st.warning("Backend not running. Showing demo data for visualization.")

    # ---- DEMO DATA (for cloud deployment) ----
    demo_df = pd.DataFrame({
        "timestamp": pd.date_range(
            end=pd.Timestamp.now(),
            periods=12,
            freq="min"
        ),
        "deauth_count": [0, 1, 0, 3, 6, 12, 25, 18, 9, 4, 1, 0],
        "risk": [
            "LOW", "LOW", "LOW", "LOW",
            "MEDIUM", "HIGH", "HIGH",
            "MEDIUM", "LOW", "LOW", "LOW", "LOW"
        ]
    })

    demo_df["timestamp"] = pd.to_datetime(demo_df["timestamp"])
    demo_df = demo_df.set_index("timestamp")

    st.subheader("📈 Deauthentication Activity (Demo)")
    st.line_chart(demo_df["deauth_count"])

    st.subheader("🚨 Risk Timeline (Demo)")
    st.dataframe(demo_df.reset_index(), use_container_width=True)

    st.markdown("---")
    st.markdown(
        "> **Did you know?** With less than ₹5,000 worth of hardware, attackers can "
        "force Wi-Fi clients to disconnect using unauthenticated deauthentication frames "
        "in WPA2 networks."
    )

    st.stop()

# ---------------- REAL DATA MODE ----------------
df = pd.read_csv(DATA_PATH)

if df.empty:
    st.warning("No events recorded yet.")
    st.stop()

# Normalize timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
df = df.sort_values("timestamp")
df = df.set_index("timestamp")

# ---------------- VISUALS ----------------
st.subheader("📈 Deauthentication Activity")
st.line_chart(df["deauth_count"])

st.subheader("🚨 Detected Events")
st.dataframe(df.reset_index(), use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "> **Note:** Backend PCAP ingestion runs locally due to wireless monitor-mode "
    "requirements. This frontend is cloud-hosted for live visualization."
)
