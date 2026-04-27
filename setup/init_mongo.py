from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://root:root@localhost:27017/admin")
db = client["patient_monitoring"]

# Collection patients
db.patients.drop()
patients = [
    {"patientId": f"P-{str(i).zfill(4)}", "name": f"Patient {i}",
     "dateOfBirth": "1980-01-01", "gender": "M" if i%2==0 else "F",
     "ward": ["Cardiology","ICU","Neurology"][i%3],
     "medicalHistory": ["hypertension"],
     "assignedDevices": [f"DEV-HR-{str(i).zfill(3)}"]}
    for i in range(1, 11)
]
db.patients.insert_many(patients)

# Collection devices
db.devices.drop()
devices = []
for metric, prefix, dev_type in [
    ("HeartRate","DEV-HR","HeartRateMonitor"),
    ("Temperature","DEV-TM","ThermometerSensor"),
    ("OxygenLevel","DEV-OX","PulseOximeter"),
]:
    for i in range(1, 4):
        devices.append({
            "deviceId": f"{prefix}-{str(i).zfill(3)}",
            "type": dev_type,
            "manufacturer": "Philips",
            "capabilities": [metric],
            "patientId": f"P-{str(i).zfill(4)}",
            "installedAt": datetime(2024, 1, 10, 8, 0, 0),
        })
db.devices.insert_many(devices)

# Index sur sensor_readings
db.sensor_readings.create_index([("patientId", 1), ("timestamp", -1)])
db.sensor_readings.create_index([("alertLevel", 1)])

print(" MongoDB initialisé : patients, devices, sensor_readings")
print(f"   Patients : {db.patients.count_documents({})}")
print(f"   Devices  : {db.devices.count_documents({})}")
