import os
import json
import asyncio
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["SESSION"]

SOURCE = os.environ["SOURCE_CHANNEL"]
DEST = os.environ["DESTINATION_CHAT"]

# جلوگیری از اجرای دوباره داخل یک request
RUNNING = False


async def run_forward():
    global RUNNING

    if RUNNING:
        return "already_running"

    RUNNING = True

    try:
        client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
        await client.start()

        messages = await client.get_messages(SOURCE, limit=10)
        await client.forward_messages(DEST, messages, SOURCE)

        await client.disconnect()

        return len(messages)

    finally:
        RUNNING = False


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            qs = parse_qs(urlparse(self.path).query)

            if qs.get("run", ["0"])[0] != "1":
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"status":"ignored"}')
                return

            count = asyncio.run(run_forward())

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
