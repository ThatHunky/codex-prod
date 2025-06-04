from aiogram import Router, types
from aiogram.filters import CommandStart


try:
    from bot.memory import add_message, clear_history, get_history
except ImportError:  # pragma: no cover - fallback for `python bot/main.py`
    from memory import add_message, clear_history, get_history


# Import relative to package when run with `python -m bot.main`

try:
    from bot.gemini import generate_response
except ImportError:  # pragma: no cover - fallback for `python bot/main.py`
    from gemini import generate_response


router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    if message.from_user:
        await clear_history(message.from_user.id)
    await message.answer("Welcome to the Gemini bot!")


@router.message()
async def echo_with_gemini(message: types.Message) -> None:
    if not message.text:
        return
    user_id = message.from_user.id if message.from_user else 0
    history = await get_history(user_id)
    response = await generate_response(message.text, history)
    await message.answer(response)
    await add_message(user_id, "user", message.text)
    await add_message(user_id, "model", response)
