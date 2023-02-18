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

        elif(request == "JoinResponse"):
            print(result["status"])

        elif(request == "LeaveResponse"):
            print(result["status"])

        elif(request == "PublishResponse"):
            print(result["status"])

        elif(request == "GetResponse"):
            if(result["status"] == "FAILED"):
                print(result["status"])
            else:
                data = result["data"]
                print(data)
            


    while True:
        print("\nChoose an option:")
        print("1. Get Server List")
        print("2. Join a server")
        print("3. Leave a server")
        print("4. Get Articles")
        print("5. Publish Article")
        print("6. Quit")

        choice = input("Enter your choice:\n")

        if choice == "1":
            channel.basic_publish(exchange='', routing_key='registry_server', body=json.dumps({"name": client_id, "request": "GetServerList"}))
            channel.basic_consume(queue=client_id, on_message_callback=callback, auto_ack=True) 

        elif choice == "2":
            server_name = input("\nEnter the name of the server you want to join-\n")
            channel.basic_publish(exchange='', routing_key=server_name, body=json.dumps({"name": client_id, "routing_key":client_id, "request": "JoinServer"}))
            channel.basic_consume(queue=client_id, on_message_callback=callback, auto_ack=True)

        elif choice == "3":
            server_name_leave = input("\nEnter the name of the server you want to leave-\n")
            channel.basic_publish(exchange='', routing_key=server_name_leave, body=json.dumps({"name": client_id, "routing_key":client_id, "request": "LeaveServer"}))
            channel.basic_consume(queue=client_id, on_message_callback=callback, auto_ack=True)

        elif choice == "4":
            serv = input("Enter the server name you want to get articles from:\n")
            typ = input("Enter the type:\n")
            auth = input("Enter the author:\n")
            date = input("Enter the date(DD/MM/YYYY):\n")
            channel.basic_publish(exchange='', routing_key=serv, body=json.dumps({"name": client_id, "routing_key":client_id, "request": "GetArticles", "type": typ, "author": auth, "date": date}))
            channel.basic_consume(queue=client_id, on_message_callback=callback, auto_ack=True)


        elif choice == "5":
            ser = input("Enter the server name you want to publish to:\n")
            ty = input("Enter the type:\n")
            author = input("Enter the author:\n")
            content = input("Enter the content of article:\n")
            if not (ty and author and content):
                print("Illegal Format!")
                break
            channel.basic_publish(exchange='', routing_key=ser, body=json.dumps({"name": client_id, "routing_key":client_id, "request": "PublishArticle", "type": ty, "author": author, "content": content}))
            channel.basic_consume(queue=client_id, on_message_callback=callback, auto_ack=True)
        
        elif choice == "6":
            break

        else:
            continue

        connection.process_data_events(time_limit=1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)