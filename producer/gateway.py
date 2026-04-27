from kafka import KafkaProducer
from pymongo import MongoClient
import json, time, random, pandas as pd
from datetime import datetime

# ── Thresholds ──────────────────────────────────────────────
THRESHOLDS = {
    "HeartRate":       {"normal":(60,100), "warning":(50,120), "critical":(40,150)},
    "Temperature":     {"normal":(36.1,37.2), "warning_high":38.0, "critical_high":39.5, "critical_low":35.0},
    "OxygenLevel":     {"warning_low":93, "critical_low":90},
    "BloodPressure":   {"warning_high":130, "critical_high":180, "critical_low":70},
    "RespiratoryRate": {"normal":(12,20), "warning":(10,24), "critical":(8,30)},
}

TOPIC_MAP = {
    "HeartRate":       "patient.heartrate",
    "Temperature":     "patient.temperature",
    "OxygenLevel":     "patient.oxygenlevel",
    "BloodPressure":   "patient.bloodpressure",
    "RespiratoryRate": "patient.respiratoryrate",
}

def classify(metric, value):
    if metric == "HeartRate":
        if value < 40 or value > 150: return "critical"
        if value < 50 or value > 120: return "warning"
        return "normal"
    if metric == "Temperature":
        if value > 39.5 or value < 35: return "critical"
        if value > 38.0: return "warning"
        return "normal"
    if metric == "OxygenLevel":
        if value < 90: return "critical"
        if value < 93: return "warning"
        return "normal"
    if metric == "BloodPressure":
        if value > 180 or value < 70: return "critical"
        if value > 130: return "warning"
        return "normal"
    if metric == "RespiratoryRate":
        if value < 8 or value > 30: return "critical"
        if value < 10 or value > 24: return "warning"
        return "normal"
    return "normal"

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
mongo = MongoClient("mongodb://root:root@localhost:27017/admin")
col = mongo["patient_monitoring"]["sensor_readings"]

df = pd.read_csv("Data/sensors.csv")
print(f"🚀 Démarrage du simulateur IoT — {len(df)} enregistrements")

for i, row in df.iterrows():
    doc = {
        "timestamp":  datetime.utcnow().isoformat() + "Z",
        "patientId":  row["PatientID"],
        "deviceId":   row["DeviceID"],
        "metric":     row["Metric"],
        "value":      row["Value"],
        "unit":       row["Unit"],
        "alertLevel": classify(row["Metric"], row["Value"]),
    }

    # Envoyer au topic principal
    topic = TOPIC_MAP.get(row["Metric"], "patient.heartrate")
    producer.send(topic, doc)

    # Envoyer au topic d'alerte si nécessaire
    if doc["alertLevel"] == "critical":
        producer.send("patient.alerts.critical", doc)
        print(f"🚨 CRITICAL | {doc['patientId']} | {doc['metric']} = {doc['value']} {doc['unit']}")
    elif doc["alertLevel"] == "warning":
        producer.send("patient.alerts.warning", doc)
        print(f"⚠️  WARNING  | {doc['patientId']} | {doc['metric']} = {doc['value']} {doc['unit']}")

    # Persister dans MongoDB
    col.insert_one(doc)

    producer.flush()
    time.sleep(1)  # 1 message/seconde

producer.close()
