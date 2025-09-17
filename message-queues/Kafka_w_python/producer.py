import json
import time

from kafka import KafkaProducer
from tqdm import tqdm

# This address should now work because of the port mapping
# and the advertised listener setting in docker-compose.
bootstrap_servers = ["localhost:9092"]
topic_name = "my-topic"


def generate_message_with_size(message_id, target_size_kb):
    base_message = {
        "number": message_id,
        "message": f"Message {message_id}",
        "distribution_method": "default_round_robin",
        "timestamp": time.time(),
    }

    base_size = len(json.dumps(base_message).encode("utf-8"))
    target_size_bytes = int(target_size_kb * 1024)  # convert KB to bytes

    if target_size_kb == 0.1:
        buffer = 17
    elif target_size_kb == 0.5:
        buffer = 27
    elif target_size_kb == 1:
        buffer = 39

    padding_needed = max(0, target_size_bytes - base_size - buffer)
    base_message["padding"] = "x" * padding_needed

    return base_message


MESSAGE_SIZE_KB = 0.1
# MESSAGE_SIZE_KB = 0.5
# MESSAGE_SIZE_KB = 1
# NUM_MESSAGES = 1000
NUM_MESSAGES = 100000

try:
    # 1. Create a KafkaProducer instance
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        # Encode messages as JSON
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    print(f"Successfully connected to Kafka broker at {bootstrap_servers}")

    # 2. Send messages
    print(f"Sending {NUM_MESSAGES} messages of {MESSAGE_SIZE_KB}KB each...")

    start_time = time.time()
    for i in tqdm(range(NUM_MESSAGES)):
        message = generate_message_with_size(i, MESSAGE_SIZE_KB)

        # Calculate actual message size for verification
        # actual_size = len(json.dumps(message).encode("utf-8"))
        # print(f"Sending message {i}: {actual_size} bytes ({actual_size / 1024:.2f}KB)")

        # Send the message to the specified topic
        # future = producer.send(topic_name, value=message)
        producer.send(topic_name, value=message)

        # try:
        # Block until the message is sent and get metadata
        # record_metadata = future.get(timeout=10)
        # print(
        #     f"Message sent to topic '{record_metadata.topic}' "
        #     f"partition {record_metadata.partition} "
        #     f"with offset {record_metadata.offset}"
        # )
        # except Exception as e:
        #     print(f"Error sending message: {e}")

        # time.sleep(1)

    end_time = time.time()
    print(
        f"Time taken for {NUM_MESSAGES} messages of {MESSAGE_SIZE_KB}KB each: {end_time - start_time:.2f} seconds"
    )

finally:
    # 3. Flush and close the producer
    if "producer" in locals() and producer.bootstrap_connected():
        producer.flush()
        print("All messages flushed.")
        producer.close()
        print("Producer closed.")
