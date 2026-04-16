import json
import datetime
import os

LOG_FILE = "logs/audit.log"

def log_event(event, message):
    os.makedirs("logs", exist_ok=True)

    entry = {
        "timestamp": str(datetime.datetime.utcnow()),
        "event": event,
        "message": message
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
