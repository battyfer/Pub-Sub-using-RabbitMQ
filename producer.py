import pika

# To establish the connection with RabbitMQ server
# we added localhost as it is for local machine but if we want to connect to a server the 
# we will add the IP address of the server here.
connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

# Declaring the receiver's queue
channel.queue_declare(queue='letterbox')

message = 'Hello! This is my first message'

# We added empty string in exchange as we are using the default exchange here and using routing_key
# to specify which queue we want to send the msg to.
channel.basic_publish(exchange = '', routing_key = 'letterbox', body = message)

print(f"sent message: {message}")

connection.close()

