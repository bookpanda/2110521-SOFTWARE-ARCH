import json
import threading
import time

from kafka import KafkaConsumer

# --- Configuration ---
BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC_NAME = "my-topic"
GROUP_ID = "high-speed-group"
NUM_CONSUMERS = 4

# --- Timing state ---
timing_lock = threading.Lock()
start_time = None
end_time = None
msg_count = 0


def consume_in_parallel(consumer_id: str):
    global start_time, end_time, msg_count

    print(f"[{consumer_id}] Starting consumer for group '{GROUP_ID}'...")

    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=BOOTSTRAP_SERVERS,
            group_id=GROUP_ID,
            auto_offset_reset="earliest",
            consumer_timeout_ms=10000,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )

        print(f"[{consumer_id}] is now listening...")

        for message in consumer:
            with timing_lock:
                # Record the first message time once
                if start_time is None:
                    start_time = time.time()
                # Update last seen message time every time
                end_time = time.time()
            msg_count += 1
            # print(
            #     f"[{consumer_id}] Partition {message.partition} | "
            #     f"Received: {message.value}"
            # )
            # Simulate work
            # time.sleep(0.5)

        print(
            f"[{consumer_id}] Timed out. Shutting down. Received {msg_count} messages."
        )

    except Exception as e:
        print(f"[{consumer_id}] An error occurred: {e}")
    finally:
        if "consumer" in locals():
            consumer.close()
            print(f"[{consumer_id}] Consumer closed.")


if __name__ == "__main__":
    threads = []
    print(f"--- Starting {NUM_CONSUMERS} consumers in group '{GROUP_ID}' ---")

    for i in range(NUM_CONSUMERS):
        thread = threading.Thread(
            target=consume_in_parallel, args=(f"Consumer-{i + 1}",)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("--- All consumer threads have finished ---")

    if start_time and end_time:
        total_time = end_time - start_time
        print(f"Total processing time: {total_time:.3f} seconds")
        print(f"Throughput: {msg_count / total_time:.3f} messages/s")
    else:
        print("No messages were consumed.")
