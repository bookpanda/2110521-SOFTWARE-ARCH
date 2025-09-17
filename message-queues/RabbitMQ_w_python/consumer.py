import json
import threading
import time

import pika

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "test-queue"
NUM_CONSUMERS = 4

timing_lock = threading.Lock()
start_time = None
end_time = None
msg_count = 0


def consume_in_parallel(consumer_id: str):
    global start_time, end_time, msg_count

    print(f"[{consumer_id}] Starting consumer for queue '{QUEUE_NAME}'...")

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST)
        )
        channel = connection.channel()

        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        channel.basic_qos(prefetch_count=1)

        print(f"[{consumer_id}] is now listening...")

        def callback(ch, method, properties, body):
            global start_time, end_time, msg_count

            with timing_lock:
                if start_time is None:
                    start_time = time.time()
                end_time = time.time()
                msg_count += 1

            try:
                message_data = json.loads(body.decode("utf-8"))

                # print(
                #     f"[{consumer_id}] Received: {message_data}"
                # )

                # Simulate work (commented out for performance testing)
                # time.sleep(0.5)

                ch.basic_ack(delivery_tag=method.delivery_tag)

            except Exception as e:
                print(f"[{consumer_id}] Error processing message: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

        timeout_start = time.time()
        timeout_duration = 10

        while time.time() - timeout_start < timeout_duration:
            try:
                connection.process_data_events(time_limit=1)

                with timing_lock:
                    if end_time and (time.time() - end_time) < 2:
                        timeout_start = time.time()

            except Exception as e:
                print(f"[{consumer_id}] Error in event processing: {e}")
                break

        print(f"[{consumer_id}] Timed out. Shutting down.")

    except Exception as e:
        print(f"[{consumer_id}] An error occurred: {e}")
    finally:
        if "connection" in locals():
            try:
                connection.close()
                print(f"[{consumer_id}] Consumer closed.")
            except:
                pass


if __name__ == "__main__":
    threads = []
    print(f"--- Starting {NUM_CONSUMERS} consumers for queue '{QUEUE_NAME}' ---")

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
        print(f"Total messages consumed: {msg_count}")
    else:
        print("No messages were consumed.")
