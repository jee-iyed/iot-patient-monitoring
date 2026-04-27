from kafka.admin import KafkaAdminClient, NewTopic
import time

time.sleep(5)  # attendre que Kafka démarre

admin = KafkaAdminClient(bootstrap_servers="localhost:9092", client_id="setup")

topics = [
    NewTopic(name="patient.heartrate",       num_partitions=3, replication_factor=1),
    NewTopic(name="patient.temperature",     num_partitions=3, replication_factor=1),
    NewTopic(name="patient.oxygenlevel",     num_partitions=3, replication_factor=1),
    NewTopic(name="patient.bloodpressure",   num_partitions=3, replication_factor=1),
    NewTopic(name="patient.respiratoryrate", num_partitions=3, replication_factor=1),
    NewTopic(name="patient.alerts.critical", num_partitions=1, replication_factor=1),
    NewTopic(name="patient.alerts.warning",  num_partitions=1, replication_factor=1),
]

existing = admin.list_topics()
new_topics = [t for t in topics if t.name not in existing]

if new_topics:
    admin.create_topics(new_topics=new_topics, validate_only=False)
    print(f" {len(new_topics)} topics créés")
else:
    print(" Topics déjà existants")

admin.close()
