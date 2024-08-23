#этот файл мы используем для получения клиента Telegram и всех массовых чатов аккаунта

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerEmpty



class Client:
    def get_client(api_id, api_hash, phone):
        client = TelegramClient(phone,api_id,api_hash)
        return client
    def get_chats(client):
        chats = []
        last_date = None
        size_chats = 200
        groups=[]

        result = client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=size_chats,
                hash = 0
            ))
        chats.extend(result.chats)

        for chat in chats:
            try:
                if chat.megagroup== True:
                    groups.append(chat)
            except:
                continue
        
        
        return groups
        
       