FROM python:3.11-slim AS base
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim AS final
WORKDIR /app
COPY --from=base /install /usr/local
COPY . .
CMD ["python", "bot/main.py"]
