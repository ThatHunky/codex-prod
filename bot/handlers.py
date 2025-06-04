from aiogram import Router, types
from aiogram.filters import Command, CommandStart


try:
    from bot.memory import add_message, clear_history, get_history
except ImportError:  # pragma: no cover - fallback for `python bot/main.py`
    from memory import add_message, clear_history, get_history


# Import relative to package when run with `python -m bot.main`

try:
    from bot.gemini import generate_image, generate_response
except ImportError:  # pragma: no cover - fallback for `python bot/main.py`
    from gemini import generate_image, generate_response


router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    if message.from_user:
        await clear_history(message.from_user.id)
    await message.answer("Welcome to the Gemini bot!")


@router.message(Command("new_chat"))
async def new_chat_handler(message: types.Message) -> None:
    """Clear the user's chat history."""
    if message.from_user:
        await clear_history(message.from_user.id)
    await message.answer("Started a new chat.")


@router.message(Command("image"))
async def image_handler(message: types.Message) -> None:
    """Generate an image from the provided prompt."""
    if not message.text:
        return
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Usage: /image <prompt>")
        return
    img_data = await generate_image(args[1])
    await message.answer_photo(types.BufferedInputFile(img_data, "image.png"))


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
