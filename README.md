# notesy

A tiny notes app. Markdown, GraphQL, deploys to fly.

## Run locally

```bash
cp .env.example .env
uv sync
uv run uvicorn app.main:app --reload
```

Open http://localhost:8000.

## Deploy

```bash
fly launch
fly deploy
```

## License

MIT
