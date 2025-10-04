# Contoso Expense (Backend)

## Quick Start

```bash
cp .env.example .env
docker compose up -d
uv venv && source .venv/bin/activate
uv add "fastapi" "uvicorn[standard]" "sqlalchemy[asyncio]" "asyncpg" \
       "pydantic-settings" "python-jose[cryptography]" "passlib[bcrypt]"
uv run uvicorn app.main:app --reload
