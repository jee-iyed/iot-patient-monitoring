import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)
np.random.seed(42)

patients = [f"P-{str(i).zfill(4)}" for i in range(1, 11)]
devices = {
    "HeartRate":       [f"DEV-HR-{str(i).zfill(3)}" for i in range(1, 5)],
    "Temperature":     [f"DEV-TM-{str(i).zfill(3)}" for i in range(1, 4)],
    "OxygenLevel":     [f"DEV-OX-{str(i).zfill(3)}" for i in range(1, 4)],
    "BloodPressure":   [f"DEV-BP-{str(i).zfill(3)}" for i in range(1, 3)],
    "RespiratoryRate": [f"DEV-RR-{str(i).zfill(3)}" for i in range(1, 3)],
}
metrics_config = {
    "HeartRate":       ("bpm",            55, 105),
    "Temperature":     ("°C",             36.0, 38.5),
    "OxygenLevel":     ("SpO2 %",         91, 100),
    "BloodPressure":   ("mmHg",           75, 145),
    "RespiratoryRate": ("breaths/min",    11, 26),
}

records = []
start_time = datetime(2024, 3, 1, 0, 0, 0)

for i in range(10000):
    patient = random.choice(patients)
    metric  = random.choice(list(metrics_config.keys()))
    unit, low, high = metrics_config[metric]
    device  = random.choice(devices[metric])
    value   = round(random.uniform(low, high), 1)
    ts      = start_time + timedelta(seconds=i * 30)

    records.append({
        "Timestamp": ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "PatientID": patient,
        "DeviceID":  device,
        "Metric":    metric,
        "Value":     value,
        "Unit":      unit,
    })

df = pd.DataFrame(records)
df.to_csv("Data/sensors.csv", index=False)
print(f"Dataset généré : {len(df)} lignes")
print(df.head())
