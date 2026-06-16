import os
import json
from telethon import TelegramClient
from telethon.sessions import StringSession
from http.server import BaseHTTPRequestHandler

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["SESSION"]

SOURCE = os.environ["SOURCE_CHANNEL"]
DEST = os.environ["DESTINATION_CHAT"]


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            result = self.run_forward()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(result).encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def run_forward(self):

        client = TelegramClient(
            StringSession(SESSION),
            API_ID,
            API_HASH
        )

        with client:
            messages = client.get_messages(SOURCE, limit=10)

            client.forward_messages(
                DEST,
                messages,
                SOURCE
            )

        return {
            "status": "done",
            "count": len(messages)
        }