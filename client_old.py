#!/usr/bin/env python
import pika, sys, os
import json
import uuid

def main():
    client_id = str(uuid.uuid4())
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(client_id)

    def callback(ch, method, properties, body):
        result = json.loads(body)
        request = result["request"]
        if(request == "server_list"):
            print(result["server"])
            server_name = input("Enter the name of the server you want to join\n")
            channel.basic_publish(exchange='', routing_key=server_name, body=json.dumps({"name": client_id, "routing_key":client_id, "request": "JoinServer"}))

        elif(request == "JoinResponse"):
            print(result["status"])

    channel.basic_publish(exchange='', routing_key='registry_server', body=json.dumps({"name": client_id, "request": "GetServerList"}))

    
    channel.basic_consume(queue=client_id, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)