import json
import time

import pika
from tqdm import tqdm


def generate_message_with_size(message_id, target_size_kb):
    base_message = {
        "message_id": message_id,
        "producer": "rabbitmq_size_test",
    }

    base_size = len(json.dumps(base_message).encode("utf-8"))
    target_size_bytes = int(target_size_kb * 1024)

    # minimum msg size is alrady 117 bytes
    buffer = 0
    if target_size_kb == 0.5:
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


def main():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        channel = connection.channel()

        channel.queue_declare(queue="test-queue", durable=True)

        start_time = time.time()
        successful_sends = 0

        for i in tqdm(range(NUM_MESSAGES)):
            message = generate_message_with_size(i, MESSAGE_SIZE_KB)
            message_body = json.dumps(message)

            actual_size = len(message_body.encode("utf-8"))

            channel.basic_publish(
                exchange="",
                routing_key="test-queue",
                body=message_body,
                properties=pika.BasicProperties(delivery_mode=2),
            )

            successful_sends += 1
            # print(f"Message {i}: {actual_size} bytes ({actual_size / 1024:.3f}KB)")

        end_time = time.time()
        total_time = end_time - start_time
        throughput = successful_sends / total_time if total_time > 0 else 0
        total_data_kb = successful_sends * MESSAGE_SIZE_KB
        data_throughput = total_data_kb / total_time if total_time > 0 else 0

        print("\nPerformance Summary:")
        print(f"   Messages sent: {successful_sends}/{NUM_MESSAGES}")
        print(f"   Total time: {total_time:.2f} seconds")
        print(f"   Throughput: {throughput:.2f} messages/sec")
        print(f"   Data sent: {total_data_kb:.2f} KB")
        print(f"   Data throughput: {data_throughput:.2f} KB/sec")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if "connection" in locals():
            connection.close()
            print("Connection closed.")


if __name__ == "__main__":
    main()
