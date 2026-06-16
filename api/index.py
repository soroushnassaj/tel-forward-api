import os
import json
from http.server import BaseHTTPRequestHandler
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["SESSION"]

SOURCE = os.environ["SOURCE_CHANNEL"]
DEST = os.environ["DESTINATION_CHAT"]


def run_forward():
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

    with client:
        messages = list(client.get_messages(SOURCE, limit=10))  

        client.forward_messages(DEST, messages, SOURCE)

        return len(messages)


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            count = run_forward()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps({
                "status": "done",
                "count": count
            }).encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
