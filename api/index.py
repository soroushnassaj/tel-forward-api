import os
import json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler

from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["SESSION"]


def get_messages(channel):
    client = TelegramClient(
        StringSession(SESSION),
        API_ID,
        API_HASH
    )

    with client:
        messages = client.loop.run_until_complete(
            client.get_messages(channel, limit=10)
        )

        result = []

        for msg in messages:
            result.append({
                "id": msg.id,
                "text": msg.message,
                "date": msg.date.isoformat() if msg.date else None,
                "views": getattr(msg, "views", None),
            })

        return result


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            query = parse_qs(urlparse(self.path).query)

            channel = query.get("channel", [None])[0]

            if not channel:
                raise Exception("channel parameter is required")

            data = get_messages(channel)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                json.dumps(
                    {
                        "count": len(data),
                        "messages": data
                    },
                    ensure_ascii=False
                ).encode("utf-8")
            )

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
