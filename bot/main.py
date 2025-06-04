import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv


# Allow running the script directly or as a module
try:
    # When executed with `python -m bot.main` or in Docker
    from bot.handlers import router
except ImportError:  # pragma: no cover - fallback for `python bot/main.py`
    from handlers import router



async def main() -> None:
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_TOKEN is not set")

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token)
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass

