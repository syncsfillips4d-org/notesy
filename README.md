# notesy

Tiny notes app. FastAPI + Strawberry GraphQL. Deploys to fly.

Live demo: https://notesy-801183.fly.dev

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
fly deploy
```

## License

MIT
