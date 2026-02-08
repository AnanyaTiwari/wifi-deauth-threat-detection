import time
import csv
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from pcap_parser import extract_features
from ml_model import get_model, score_anomaly

ROOT = Path(__file__).resolve().parents[1]
PCAP_DIR = ROOT / "pcaps"
DATA_DIR = ROOT / "data"
TIMELINE = DATA_DIR / "timeline.csv"

DATA_DIR.mkdir(exist_ok=True)

if not TIMELINE.exists():
    with open(TIMELINE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "deauth_count", "deauth_rate", "risk"])


def wait_for_file_ready(path, timeout=5):
    start = time.time()
    last_size = -1
    while time.time() - start < timeout:
        try:
            size = os.path.getsize(path)
            if size > 0 and size == last_size:
                return True
            last_size = size
        except FileNotFoundError:
            pass
        time.sleep(0.2)
    return False


model = get_model()


class PCAPHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.src_path.endswith(".pcap"):
            return

        if not wait_for_file_ready(event.src_path):
            return

        try:
            features = extract_features(event.src_path)
            score = score_anomaly(model, features)
        except Exception as e:
            print(f"[ERROR] {e}")
            return

        if score < -0.5:
            risk = "HIGH"
        elif score < -0.2:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        with open(TIMELINE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                int(time.time()),
                features["deauth_count"],
                features["deauth_rate_per_min"],
                risk
            ])

        print(f"[INFO] Logged | Risk={risk} | Score={round(score,3)}")


if __name__ == "__main__":
    observer = Observer()
    observer.schedule(PCAPHandler(), str(PCAP_DIR), recursive=False)
    observer.start()

    print("[*] PCAP watcher running (REAL MODE)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
