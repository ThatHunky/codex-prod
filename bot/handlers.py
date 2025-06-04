from aiogram import Router, types
from aiogram.filters import CommandStart

from .gemini import generate_response

router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    await message.answer("Welcome to the Gemini bot!")


@router.message()
async def echo_with_gemini(message: types.Message) -> None:
    if not message.text:
        return
    response = await generate_response(message.text)
    await message.answer(response)

