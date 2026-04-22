# SMTP to Telegram

A lightweight SMTP relay that receives emails and forwards them to Telegram. Drop-in replacement for [smtp-gotify](https://hub.docker.com/r/piedelivery/smtp-gotify) but targeting Telegram instead of Gotify.

Point any application's SMTP settings at this container and every email it receives will be forwarded as a Telegram message — subject, sender, and body.

---

## Quick start — Docker Hub (easiest)

The pre-built image supports both `linux/amd64` and `linux/arm64`. No need to clone the repo.

### Option A — docker compose (recommended)

Create a `docker-compose.yaml`:

```yaml
services:
  smtp-telegram:
    image: daimik/smtp-telegram:latest
    container_name: smtp-telegram
    environment:
      - TELEGRAM_BOT_TOKEN=your-bot-token
      - TELEGRAM_CHAT_ID=your-chat-id
    ports:
      - "2525:25"
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
```

```sh
docker compose up -d
```

### Option B — plain docker run

```sh
docker run -d \
  --name smtp-telegram \
  --restart unless-stopped \
  -p 2525:25 \
  -e TELEGRAM_BOT_TOKEN=your-bot-token \
  -e TELEGRAM_CHAT_ID=your-chat-id \
  daimik/smtp-telegram:latest
```

---

## Quick start — build from source

```sh
git clone https://github.com/daimik/smtp-telegram.git
cd smtp-telegram
docker compose up -d --build
```

---

## Multiple instances

Run as many containers as you need, each on a different port. Useful when different applications should post to different Telegram chats or bots.

```yaml
services:
  smtp-telegram-deluge:
    image: daimik/smtp-telegram:latest
    container_name: smtp-telegram-deluge
    environment:
      - TELEGRAM_BOT_TOKEN=your-bot-token
      - TELEGRAM_CHAT_ID=-100123456789
    ports:
      - "2525:25"
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true

  smtp-telegram-proxmox:
    image: daimik/smtp-telegram:latest
    container_name: smtp-telegram-proxmox
    environment:
      - TELEGRAM_BOT_TOKEN=your-bot-token
      - TELEGRAM_CHAT_ID=-100987654321
    ports:
      - "2526:25"
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true

  smtp-telegram-nas:
    image: daimik/smtp-telegram:latest
    container_name: smtp-telegram-nas
    environment:
      - TELEGRAM_BOT_TOKEN=your-bot-token
      - TELEGRAM_CHAT_ID=-100111222333
    ports:
      - "2527:25"
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
```

Each container listens on port 25 internally — just change the external port mapping and the Telegram chat ID per instance.

---

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Yes | Telegram Bot API token (from [@BotFather](https://t.me/BotFather)) |
| `TELEGRAM_CHAT_ID` | Yes | Target chat/group ID (use [@userinfobot](https://t.me/userinfobot) or `-100...` for groups) |

---

## Getting your Telegram credentials

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot`, follow the prompts — you'll receive a **bot token**
3. Add the bot to your target chat/group
4. To get the **chat ID**, message [@userinfobot](https://t.me/userinfobot) (for personal chats) or check the bot API: `https://api.telegram.org/bot<token>/getUpdates`

---

## Testing

Send a test email with PowerShell:

```powershell
Send-MailMessage -From "test@example.com" -To "test@localhost" -Subject "Test" -Body "Hello from SMTP" -SmtpServer "10.10.1.21" -Port 2525
```

Or with `swaks` (Linux):

```sh
swaks --to test@localhost --from sender@example.com --server 10.10.1.21:2525 \
  --header "Subject: Test" --body "Hello from SMTP"
```

---

## Useful commands

```sh
docker compose logs -f              # stream logs
docker compose down                 # stop and remove containers
docker compose pull && docker compose up -d  # update to latest image
```
