import uuid
import random
import time
from datetime import datetime, timezone
from faker import Faker
import psycopg2
import json

fake = Faker()

resorts = ["Alpine Peak", "SnowHeaven", "Ice Valley"]
lifts = ["LiftA", "LiftB", "LiftC"]
gates = ["Gate1", "Gate2", "Gate3"]
statuses = ["success", "denied"]

# Databse
conn = psycopg2.connect(
    dbname="ski_db",
    user="postgres",
    password="secret",
    host="localhost"
)

# generate the random information
def simulate_scan():
    return {
        "scan_time": datetime.now(timezone.utc),
        "skipass_id": str(uuid.uuid4()),
        "resort": random.choice(resorts),
        "lift": random.choice(lifts),
        "gate": random.choice(gates),
        "reservation_id": random.randint(1, 10),
        "client_id": random.randint(1, 24),
        "scan_status": random.choice(statuses),
        "metadata": {
            "temp": random.uniform(-10.0, 3.0),
            "weather": random.choice(["snow", "clear", "windy"])
        }
    }

# insert the data in the table
def insert_event(event):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO skipass_telemetry (scan_time, skipass_id, resort, lift, gate, reservation_id, client_id, scan_status, metadata)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb)
        """, (
            event["scan_time"], event["skipass_id"], event["resort"],
            event["lift"], event["gate"], event["reservation_id"],
            event["client_id"], event["scan_status"],
            json.dumps(event["metadata"])
        ))
        conn.commit()

# insert 100 information
for _ in range(100):
    insert_event(simulate_scan())
    time.sleep(0.1)

conn.close()

# print when it is ready
print("Ready")
