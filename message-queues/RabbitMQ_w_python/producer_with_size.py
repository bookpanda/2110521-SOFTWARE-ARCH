#!/usr/bin/env python3
"""
RabbitMQ Producer with Configurable Message Size
Usage: python producer_with_size.py --size 0.5 --messages 10
"""

import argparse
import json
import time

import pika


def generate_message_with_size(message_id, target_size_kb):
    """Generate a message with a specific size in KB"""
    base_message = {
        "message_id": message_id,
        "content": f"RabbitMQ test message #{message_id}",
        "timestamp": time.time(),
        "producer": "rabbitmq_size_test",
    }

    # Calculate current size
    base_size = len(json.dumps(base_message).encode("utf-8"))
    target_size_bytes = int(target_size_kb * 1024)

    # Add padding to reach target size
    padding_needed = max(0, target_size_bytes - base_size - 50)
    base_message["padding"] = "x" * padding_needed

    return base_message


def main():
    parser = argparse.ArgumentParser(
        description="RabbitMQ Producer with Configurable Message Size"
    )
    parser.add_argument(
        "--size", type=float, default=0.5, help="Message size in KB (default: 0.5)"
    )
    parser.add_argument(
        "--messages",
        type=int,
        default=10,
        help="Number of messages to send (default: 10)",
    )
    parser.add_argument(
        "--queue", type=str, default="test-queue", help="RabbitMQ queue name"
    )
    parser.add_argument("--host", type=str, default="localhost", help="RabbitMQ host")

    args = parser.parse_args()

    print(f"🚀 RabbitMQ Producer Configuration:")
    print(f"   Host: {args.host}")
    print(f"   Queue: {args.queue}")
    print(f"   Message size: {args.size}KB")
    print(f"   Number of messages: {args.messages}")
    print("-" * 50)

    try:
        # Create connection
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=args.host))
        channel = connection.channel()

        # Declare queue
        channel.queue_declare(queue=args.queue, durable=True)

        print(f"✅ Connected to RabbitMQ at {args.host}")

        # Send messages
        start_time = time.time()
        successful_sends = 0

        for i in range(args.messages):
            # Generate message with specific size
            message = generate_message_with_size(i, args.size)
            message_body = json.dumps(message)

            # Calculate actual message size
            actual_size = len(message_body.encode("utf-8"))

            # Send message
            channel.basic_publish(
                exchange="",
                routing_key=args.queue,
                body=message_body,
                properties=pika.BasicProperties(delivery_mode=2),  # Persistent
            )

            successful_sends += 1
            print(f"📤 Message {i}: {actual_size} bytes ({actual_size / 1024:.3f}KB)")

        # Performance metrics
        end_time = time.time()
        total_time = end_time - start_time
        throughput = successful_sends / total_time if total_time > 0 else 0
        total_data_kb = successful_sends * args.size
        data_throughput = total_data_kb / total_time if total_time > 0 else 0

        print("\n📊 Performance Summary:")
        print(f"   Messages sent: {successful_sends}/{args.messages}")
        print(f"   Total time: {total_time:.2f} seconds")
        print(f"   Throughput: {throughput:.2f} messages/sec")
        print(f"   Data sent: {total_data_kb:.2f} KB")
        print(f"   Data throughput: {data_throughput:.2f} KB/sec")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        if "connection" in locals():
            connection.close()
            print("🔒 Connection closed.")


if __name__ == "__main__":
    main()
