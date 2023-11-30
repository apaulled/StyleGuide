import json

import pika
import sys

from PIL import Image

from src import image_processing


def dispatch_color(piece_color):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='colors')

    color_averages = piece_color['color']
    piece_color['color'] = color_averages
    channel.basic_publish(exchange='',
                          routing_key='colors',
                          body=json.dumps(piece_color))

    print(f" [x] Sent '{piece_color}'")

    connection.close()


def consume_queues():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='pieces')

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

    piece_color = {'id': uuid,
                   'color': image_processing.primary_color(image)}

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