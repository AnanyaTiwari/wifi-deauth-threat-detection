## 🛠️ Solution
This project implements a full detection pipeline:
- PCAP ingestion and parsing
- Deauthentication burst detection
- ML-based anomaly scoring (Isolation Forest)
- Real-time SOC-style dashboard

## ⚙️ Architecture
backend/
├── pcap_parser.py # Feature extraction from PCAPs
├── pcap_watcher.py # Real-time ingestion pipeline
├── ml_model.py # Anomaly detection engine
frontend/
├── dashboard.py # SOC dashboard (Streamlit)


## 📊 Features
- Detects abnormal deauthentication bursts
- Identifies handshake capture attempts
- Learns baseline Wi-Fi behavior using ML
- Visualizes threats in real time

## 🧠 Technologies
- Python
- Scapy
- Watchdog
- scikit-learn (Isolation Forest)
- Streamlit

## 🖥️ Demo
Screenshots generated using controlled PCAP replay to validate visualization
and alerting pipelines.

## 🚀 Future Enhancements
- Live monitor-mode capture
- Email alerts for high-risk events
- WPA3 readiness checks
- Cloud deployment

---

**Author:** Ananya Tiwari  
**LinkedIn:** https://www.linkedin.com/in/ananya-tiwari-5472872b9
