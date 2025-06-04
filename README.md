# Gemini Telegram Bot

This project demonstrates a simple Telegram bot built with [aiogram](https://github.com/aiogram/aiogram) and the Gemini API. The bot replies to `/start` and forwards any other text to the Gemini API.


It calls the **Gemini 2.0 Flash** model for fast responses.



## Running locally

1. Install requirements: `pip install -r requirements.txt`
2. Create a `.env` file with your `TELEGRAM_TOKEN` and `GEMINI_API_KEY`.
3. Start the bot from the project root:

```bash
python bot/main.py
```

Alternatively, run it as a module:

```bash
python -m bot.main
```

Running `python -m main.py` inside the `bot` folder will not work due to package imports.

## Docker

A simple `Dockerfile` is provided for containerized deployments. Build and run using:

```bash
docker build -t gemini-bot .
docker run --env-file .env gemini-bot
```
