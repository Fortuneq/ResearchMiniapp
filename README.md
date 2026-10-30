# ResearchMiniapp — AI research assistant for Telegram

A Telegram Mini App that produces a **personal research report** on any topic. The user describes what they want to learn — a market analysis, technology trends, a startup ecosystem overview — and an n8n AI workflow researches it and returns a report.

<p align="center"><img src="docs/screenshots/app.jpg" width="260" alt="AI Research Assistant"></p>

## How it works

```mermaid
sequenceDiagram
    participant U as User
    participant MA as Mini App (index.html)
    participant P as proxy_server.py
    participant N as n8n workflow
    participant L as AI tools (LLM)
    U->>MA: "What do you want to learn?"
    MA->>P: POST topic
    P->>N: forward to webhook
    N->>L: research steps
    L-->>N: findings
    N-->>P: report
    P-->>MA: report
    MA-->>U: rendered report
```

## Files

```
index.html               — Mini App UI styled with Telegram theme variables
proxy_server.py          — Python proxy that forwards requests to the n8n webhook and handles CORS
server.py                — static dev server with CORS headers
Dockerfile, docker-compose-miniapp.yml, deploy.sh — deployment
```

## Run locally

```bash
python3 proxy_server.py     # set N8N_WEBHOOK_URL in the file to your n8n webhook first
python3 server.py           # http://localhost:8000
```

## Deploy

```bash
docker compose -f docker-compose-miniapp.yml up -d --build
```

See [`README-DEPLOY.md`](README-DEPLOY.md) for registering the Mini App with @BotFather.
