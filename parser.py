#файлик где прописан класс парсера, здесь мы и пробегаемся по чатам
import os
from telethon.tl.functions.messages import GetHistoryRequest






class Parser:
    def parse(client,limit,target_group):
        all_messages = []
        total_messages = 0
        total_count_limit =  0
        offset_id = 0

        with open("keywords.txt") as file:
            keywords = [row.strip() for row in file]


        history = client(GetHistoryRequest(
            peer=target_group,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        
        resend_to=int(os.getenv('resend'))
        with open("parsed.txt") as file:
            parsed_messages = [row.strip() for row in file]

        if not history.messages:
            return 'No history'
        messages = history.messages
        for message in messages:
            if str(message.id) in parsed_messages:
                continue
            else:
                for keyword in keywords:
                    if keyword in str(message.message):
                        try:
                            client.forward_messages(resend_to,message.id,from_peer=message.peer_id)
                            all_messages.append(message.message)
                            with open ('parsed.txt','a')as file:
                                file.write(f'{message.id}\n')
                        except:
                            instr=('Невозможно переслать, так как чат защищен от пересылки\n'+message.message)
                            client.send_message(resend_to,instr)
                            with open ('parsed.txt','a')as file:
                                file.write(f'{message.id}\n')
                            continue
                        print(message)
                    else:
                        continue
            offset_id = messages[len(messages) - 1].id
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break

        return all_messages