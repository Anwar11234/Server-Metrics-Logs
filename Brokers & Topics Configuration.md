# Brokers Configuration

- The Kafka cluster consists of **3 Kafka brokers**.  
- Each broker has a unique `KAFKA_BROKER_ID`, and every broker connects to a **Zookeeper** service running at port **2181**.

- All brokers use the **PLAINTEXT** protocol for communication.

- Brokers replicate the `__consumer_offsets` topic **3 times** using the environment variable:   `KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR`.

- Brokers have a **default replication factor of 3** for automatically created topics.This is set using the environment variable: `KAFKA_DEFAULT_REPLICATION_FACTOR`.

---

# Listeners

This setting tells a Kafka broker which network addresses and ports to listen on for incoming messages.

- The setup uses the `0.0.0.0` network address for all brokers, which means:  
  **"Listen on all available network interfaces."**
- One listener is for **internal (Docker)** communication.
- The other is for **external (host machine)** communication.

### Port Mapping per Broker

| Broker | External Port | Internal Port |
|--------|----------------|----------------|
| Broker 1 | 9092 | 19092 |
| Broker 2 | 9093 | 29092 |
| Broker 3 | 9094 | 39092 |

---

# Advertised Listeners

This tells Kafka brokers how they should advertise themselves to others — like clients or other brokers.

### Broker 1
- Internal: `PLAINTEXT://kafka1:19092`
- External: `PLAINTEXT_HOST://localhost:9092`

### Broker 2
- Internal: `PLAINTEXT://kafka2:29092`
- External: `PLAINTEXT_HOST://localhost:9093`

### Broker 3
- Internal: `PLAINTEXT://kafka3:39092`
- External: `PLAINTEXT_HOST://localhost:9094`

---

# Topics Configuration

## Metrics Topic
- **Number of partitions:** 3  
- **Replication Factor:** 3  
- **Retention period:** 1 Day

## Logs Topic
- **Number of partitions:** 2  
- **Replication Factor:** 3  
- **Retention period:** 1 Day