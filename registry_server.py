#!/usr/bin/env python
import pika, sys, os
import json

servers = []
max_servers = 6

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='registry_server')

    def callback(ch, method, properties, body):
        result = json.loads(body)
        request = result["request"]
        if(request == "Register"):
            server_id = result["routing_key"]
            print("JOIN REQUEST FROM", server_id)
            if(len(servers) < max_servers):
                if server_id not in servers:
                    servers.append(server_id)
                    # print("here")
                    # print(servers)
                    channel.basic_publish(exchange='', routing_key=server_id, body=json.dumps({"status":"SUCCESS", "request": "RegisterResponse"}))
                else:
                    channel.basic_publish(exchange='', routing_key=server_id, body=json.dumps({"status":"FAILED", "request": "RegisterResponse"}))
            else:
                channel.basic_publish(exchange='', routing_key=server_id, body=json.dumps({"status":"FAILED", "request": "RegisterResponse"}))

        elif(request == "GetServerList"):
            client_id = result["name"]
            print("SERVER LIST REQUEST FROM", client_id)
            channel.basic_publish(exchange='', routing_key = client_id, body=json.dumps({"server": servers, "request": "server_list"}))


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='registry_server', on_message_callback=callback, auto_ack=True)
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