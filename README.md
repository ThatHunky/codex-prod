# Gemini Telegram Bot

This project bridges Telegram messages to the [aiogram](https://github.com/aiogram/aiogram) framework and the Gemini API.
The bot replies to `/start` and forwards any other text to Gemini for quick AI-generated responses.
Conversation history is stored per user in a small SQLite database so the model can maintain context across messages.


It uses the **Gemini 2.0 Flash** model for fast responses.



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

### docker-compose

A sample `docker-compose.yml` is available for local development. Start the bot with:

```bash
docker compose up --build
```

## Development

Run linters and tests with:

```bash
ruff check .
pytest -q
```
