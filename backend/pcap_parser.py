"""
pcap_parser.py
--------------
Parses PCAP files to detect Wi-Fi deauthentication activity.

Focus:
- WPA2 weakness: unauthenticated deauth frames
- Detect abnormal deauth bursts used for handshake capture
"""

from scapy.all import rdpcap, Dot11
from collections import defaultdict


def extract_features(pcap_path: str) -> dict:
    packets = rdpcap(pcap_path)

    deauth_count = 0
    sources = defaultdict(int)
    timestamps = []

    for pkt in packets:
        if pkt.haslayer(Dot11):
            dot11 = pkt[Dot11]
            if dot11.type == 0 and dot11.subtype == 12:
                deauth_count += 1
                if dot11.addr2:
                    sources[dot11.addr2] += 1
                if hasattr(pkt, "time"):
                    timestamps.append(pkt.time)

    if timestamps:
        duration_minutes = max((max(timestamps) - min(timestamps)) / 60, 1)
    else:
        duration_minutes = 1

    deauth_rate = deauth_count / duration_minutes

    return {
        "deauth_count": deauth_count,
        "unique_deauth_sources": len(sources),
        "deauth_rate_per_min": round(deauth_rate, 2)
    }
