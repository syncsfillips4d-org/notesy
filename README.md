# notesy

Tiny notes app. FastAPI + Strawberry GraphQL. Deploys to fly.

## Run locally

```bash
cp .env.example .env
uv sync
uv run uvicorn app.main:app --env-file .env --reload
```

Open http://localhost:8000.

## Deploy

```bash
fly launch
fly secrets set BACKEND_URL=... BACKEND_KEY=... ANTHROPIC_API_KEY=... SESSION_SECRET=... OWNER_EMAIL=...
fly deploy
```

## License

MIT
