from kafka import KafkaProducer
import json, datetime

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

doc = {
    "timestamp":  datetime.datetime.utcnow().isoformat() + "Z",
    "patientId":  "P-0001",
    "deviceId":   "DEV-HR-001",
    "metric":     "HeartRate",
    "value":      180.0,   # ← valeur critique !
    "unit":       "bpm",
    "alertLevel": "critical",
}

producer.send("patient.alerts.critical", doc)
producer.flush()
print("🚨 Alerte CRITICAL injectée !")
