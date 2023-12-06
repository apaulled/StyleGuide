import json

import pika
import sys

from PIL import Image

from src import image_processing, outfit_recs


def dispatch_color(piece_color):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='colors')

    channel.basic_publish(exchange='',
                          routing_key='colors',
                          body=json.dumps(piece_color))

    print(f" [x] Sent '{piece_color}'")

    connection.close()


def dispatch_outfit(outfit):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='outfit_results')

    channel.basic_publish(exchange='',
                          routing_key='outfit_results',
                          body=json.dumps(outfit))

    print(f" [x] Sent '{outfit}'")

    connection.close()


def consume_queues():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='pieces')
    channel.queue_declare(queue='outfit_requests')
    channel.queue_declare(queue='outfit_results')

    channel.basic_consume(queue='outfit_requests',
                          auto_ack=True,
                          on_message_callback=outfit_callback)

    channel.basic_consume(queue='pieces',
                          auto_ack=True,
                          on_message_callback=piece_callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def outfit_callback(ch, method, properties, body):
    # print(body)
    decoded = json.loads(body.decode())
    uuid = decoded['userId']
    closet = decoded['userCloset']
    del(closet['userId'])

    print(closet)

    if 'color' in decoded:
        outfit = outfit_recs.color_outfit(closet, decoded['color'])
    else:
        outfit = outfit_recs.theme_outfit(closet, decoded['theme'])

    print(outfit)

    response = {'userId': uuid,
                'headWear': outfit['headWear'],
                'top': outfit['tops'],
                'bottom': outfit['bottoms'],
                'shoe': outfit['shoes'],
                'outerWear': outfit['outerWear'],
                'accessory': outfit['accessories']
                }

    print(f" [x] Received {decoded}")

    dispatch_outfit(response)


def piece_callback(ch, method, properties, body):
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
