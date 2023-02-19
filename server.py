#!/usr/bin/env python
import pika, sys, os
import json
import datetime
from datetime import datetime, date

CLIENTELE = []
MAXCLIENTS = 5
data = []

def main(server: str):
    # print(server)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=server)

    def callback(ch, method, properties, body):
        result = json.loads(body)
        request = result["request"]

        if(request == "RegisterResponse"):
            print(result["status"])

        elif(request == "JoinServer"):
            client_uuid = result["routing_key"]
            print("JOIN REQUEST FROM", client_uuid)
            if(len(CLIENTELE) < MAXCLIENTS):
                if client_uuid not in CLIENTELE:
                    CLIENTELE.append(client_uuid)
                    channel.basic_publish(exchange='', routing_key=client_uuid, body=json.dumps({"status":"SUCCESS", "request": "JoinResponse"}))
                else:
                    channel.basic_publish(exchange='', routing_key=client_uuid, body=json.dumps({"status":"SERVER ALREADY EXISTS", "request": "JoinResponse"}))
            else:
                channel.basic_publish(exchange='', routing_key=client_uuid, body=json.dumps({"status":"FAILED", "request": "JoinResponse"}))
        
        elif(request == "LeaveServer"):
            client_uuid = result["routing_key"]
            print("LEAVE REQUEST FROM", client_uuid)
            if(client_uuid not in CLIENTELE):
                channel.basic_publish(exchange='', routing_key=client_uuid, body=json.dumps({"status":"FAILED", "request": "LeaveResponse"}))
            else:
                CLIENTELE.remove(client_uuid)
                channel.basic_publish(exchange='', routing_key=client_uuid, body=json.dumps({"status":"SUCCESS", "request": "LeaveResponse"}))

        elif(request == "PublishArticle"):
            client_uuid = result["routing_key"]
            print("ARTICLES PUBLISH FROM", client_uuid)
            if(client_uuid not in CLIENTELE):
                channel.basic_publish(exchange='', routing_key=client_uuid, body=json.dumps({"status":"FAILED", "request": "PublishResponse"}))
            else:
                ty = result["type"]
                author = result["author"]
                date_pub = date.today().strftime('%d/%m/%Y') 
                # date_pub = datetime.strptime(date_pub, '%d/%m/%Y')

                content = result["content"]
                obj = {'type': ty, 'author': author, 'date': date_pub, 'content': content}
                data.append(obj)
                # print(data)
                channel.basic_publish(exchange='', routing_key=client_uuid, body=json.dumps({"status":"SUCCESS", "request": "PublishResponse"}))

        elif(request == "GetArticles"):
            client_uuid = result["routing_key"]
            print("ARTICLES REQUEST FROM", client_uuid)
            print("FOR", result["type"],"," ,result["author"],",",result["date"])
            if(client_uuid not in CLIENTELE):
               channel.basic_publish(exchange='', routing_key=client_uuid, body=json.dumps({"status":"FAILED", "request": "GetResponse"})) 
            else:
                type = result["type"]
                authorr = result["author"]
                date_get = result["date"]
                if(type and authorr):
                    filtered_data = [d for d in data if d['type'] == type and d['author'] == authorr and datetime.strptime(d['date'], '%d/%m/%Y') > datetime.strptime(date_get, '%d/%m/%Y')]
                elif(type and not(authorr)):
                    filtered_data = [d for d in data if d['type'] == type and datetime.strptime(d['date'], '%d/%m/%Y') > datetime.strptime(date_get, '%d/%m/%Y')]
                elif(authorr and not(type)):
                    filtered_data = [d for d in data if d['author'] == authorr and datetime.strptime(d['date'], '%d/%m/%Y') > datetime.strptime(date_get, '%d/%m/%Y')]
                else:
                    filtered_data = [d for d in data if datetime.strptime(d['date'], '%d/%m/%Y') > datetime.strptime(date_get, '%d/%m/%Y')]
                
                channel.basic_publish(exchange='', routing_key=client_uuid, body=json.dumps({"status":"SUCCESS", "request": "GetResponse", "data": filtered_data}))



    channel.basic_publish(exchange='', routing_key='registry_server', body=json.dumps({"name": server, "routing_key":server, "request": "Register"}))
    channel.basic_consume(queue=server, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        args = sys.argv
        main(args[1])
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)