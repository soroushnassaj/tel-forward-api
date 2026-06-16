from telethon import TelegramClient
from telethon.sessions import StringSession
import os

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["SESSION"]

SOURCE_CHANNEL = "source_channel"
DEST_CHAT = "target_chat"

async def handler(request):

    client = TelegramClient(
        StringSession(SESSION),
        API_ID,
        API_HASH
    )

    await client.connect()

    messages = await client.get_messages(
        SOURCE_CHANNEL,
        limit=10
    )

    await client.forward_messages(
        DEST_CHAT,
        messages,
        SOURCE_CHANNEL
    )

    await client.disconnect()

    return {
        "status": "done"
    }