import os
import asyncio
from aiosmtpd.controller import Controller
import httpx
from email import policy
from email.parser import BytesParser

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
SMTP_PORT = 25
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


class TelegramHandler:
    async def handle_DATA(self, server, session, envelope):
        msg = BytesParser(policy=policy.default).parsebytes(envelope.content)
        subject = msg["subject"] or "(no subject)"
        sender = msg["from"] or envelope.mail_from
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_content()
                    break
        else:
            body = msg.get_content() if msg.get_content_type() == "text/plain" else ""

        text = f"📧 <b>{subject}</b>\nFrom: {sender}\n\n{body}".strip()
        if len(text) > 4000:
            text = text[:4000] + "..."

        async with httpx.AsyncClient() as client:
            await client.post(TELEGRAM_URL, json={
                "chat_id": CHAT_ID,
                "text": text,
                "parse_mode": "HTML",
            })
        print(f"Forwarded: {subject} from {sender}")
        return "250 OK"


async def main():
    handler = TelegramHandler()
    controller = Controller(handler, hostname="0.0.0.0", port=SMTP_PORT)
    controller.start()
    print(f"SMTP-to-Telegram relay running on port {SMTP_PORT}")
    try:
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        controller.stop()


if __name__ == "__main__":
    asyncio.run(main())
