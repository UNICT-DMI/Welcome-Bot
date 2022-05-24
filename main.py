import asyncio
from telegram.bot import Bot
from os import getenv

def init_telegram_connection() -> Bot:
    token = getenv("QDBotToken")
    app = Bot(token)
    return app

async def main() -> None:
    app = init_telegram_connection()

if __name__ == '__main__':
    asyncio.run(main())