# ResearchMiniapp — AI research assistant for Telegram

A Telegram Mini App that produces a personal research report on any topic. The user describes what they want to learn, the request is forwarded to an n8n workflow that runs the AI research, and the report is shown in the app.

## How it works

```
Telegram Mini App (index.html)
        │  POST topic
        ▼
proxy_server.py  ──►  n8n webhook (AI research workflow)  ──►  report
```

- `index.html` — the Mini App UI, styled with Telegram theme variables
- `proxy_server.py` — a small Python proxy that forwards requests to the n8n webhook and handles CORS
- `server.py` — a static dev server with CORS headers

## Run locally

```bash
python3 proxy_server.py     # set N8N_WEBHOOK_URL in the file to your n8n webhook first
python3 server.py           # http://localhost:8000
```

## Deploy

```bash
docker compose -f docker-compose-miniapp.yml up -d --build
```

See [`README-DEPLOY.md`](README-DEPLOY.md) for registering the Mini App with @BotFather and deploying it.
