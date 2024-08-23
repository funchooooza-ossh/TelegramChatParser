# мэйн файлик где мы вызываем методы из других файликов
import csv
import os
import time
from dotenv import load_dotenv
from client import Client
from parser import Parser

load_dotenv()


def main():
    api_id = os.getenv("api_id")  # берем из файлика api_id
    api_hash = os.getenv("api_hash")  # api_hash
    phone = os.getenv("phone")  # номер телефона аккаунта

    client = Client.get_client(api_id, api_hash, phone)
    client.start()
    groups = Client.get_chats(client)

    for group in groups:
        limit = 100
        all_messages = Parser.parse(client, limit, group)
        with open("chats.csv", "a", encoding="UTF-8") as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            for message in all_messages:
                writer.writerow([message])
    print("Парсинг сообщений успешно выполнен.")  # Сообщение об удачном парсинге чата.


if __name__ == "__main__":
    while True:
        main()
        print("waiting for new iteration")
        time.sleep(3600)
