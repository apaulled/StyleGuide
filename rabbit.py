import json

import pika
import sys

from PIL import Image

from src import image_processing


def dispatch_color(piece_color):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='colors')

    channel.basic_publish(exchange='',
                          routing_key='colors',
                          body=json.dumps(piece_color))

    print(f" [x] Sent '{piece_color}'")

    connection.close()


def consume_queues():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='pieces')
    channel.queue_declare(queue='outfit_requests')
    channel.queue_declare(queue='outfit_results')

    channel.basic_consume(queue='pieces',
                          auto_ack=True,
                          on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def callback(ch, method, properties, body):
    # print(body)
    decoded = json.loads(body.decode())
    uuid = decoded['id']
    url = decoded['url']

    image = Image.open(url)

    key_colors = image_processing.key_colors(image)

    piece_color = {'id': uuid,
                   'primaryColor': key_colors[0],
                   'secondaryColor': key_colors[1],
                   'averageColor': image_processing.average_color(image)}

    print(f" [x] Received {uuid}")

    dispatch_color(piece_color)


if __name__ == '__main__':
    try:
        consume_queues()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            print("what")
