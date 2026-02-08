"""
app.py

Optional FastAPI backend (for future frontend/API use)
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Wi-Fi Threat Detection Backend Running"}
