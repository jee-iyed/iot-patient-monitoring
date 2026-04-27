from kafka import KafkaConsumer
import json

print("👂 Écoute des alertes critiques...")
consumer = KafkaConsumer(
    "patient.alerts.critical",
    "patient.alerts.warning",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="alert-monitor",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

for msg in consumer:
    alert = msg.value
    level = "🚨 CRITICAL" if msg.topic == "patient.alerts.critical" else "⚠️  WARNING"
    print(f"{level} | Patient: {alert['patientId']} | "
          f"{alert['metric']} = {alert['value']} {alert['unit']} | "
          f"Device: {alert['deviceId']}")
