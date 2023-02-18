import pika

def on_msg_received(channel, method, properties, body):
    print(f"New Msg recieved: {body}")

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

channel.queue_declare(queue='letterbox')

channel.basic_consume(queue = 'letterbox', auto_ack = True, on_message_callback = on_msg_received)

print("Starting Consuming. Press CTRL + C to stop")

channel.start_consuming()



