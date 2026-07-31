# CramQuest API

CramQuest is a FastAPI-based backend for managing study sessions and quests with gamification (XP, levels, titles, rewards, boss battles).

## Tech Stack

- **FastAPI** (Python 3.13)
- **SQLModel** + **async SQLAlchemy** (PostgreSQL via asyncpg)
- **Alembic** for migrations
- **JWT auth** (access token via Bearer header, refresh token in an HttpOnly cookie)
- **bcrypt** for password hashing

## Project Structure

```
├── app/
│   ├── api/v1/endpoints/  # API routers
│   ├── core/              # Database, auth, config, security
│   ├── crud/              # Async query logic
│   ├── models/            # SQLModel tables
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic (XP/level math)
│   └── main.py            # App entry point
├── migrations/            # Alembic migrations
├── requirements.txt
└── .env.example           # Copy to .env and fill in real values
```

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # then fill in DATABASE_URL, SECRET_KEY, and REFRESH_SECRET_KEY
   ```

3. Run migrations:
   ```bash
   alembic upgrade head
   ```

4. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`. Swagger/OpenAPI docs are disabled; debug via HTTP or the code.

## Models

- **User**: `id`, `username`, `email`, `password` (bcrypt-hashed), `is_active`, `is_admin`
- **Player**: `id`, `user_id`, `level`, `experience`, `next_level_xp`, `title`, streaks, boss availability — one-to-one with `User` and `Profile`
- **Profile**: `id`, `player_id`, `avatar_url`, `bio`, `mood`, `skin_url`
- **Subject**: `id`, `player_id`, `code_name`, `description`, `difficulty`
- **Quest**: `id`, `subject_id`, `description`, `difficulty`, `status`, `created_at`
- **StudySession**: `id`, `player_id`, `quest_id`, `subject_id`, `start_time`, `end_time`, `actual_complete_time`, `xp_earned`, `status`
- Plus **Task**, **Material**, **WeeklyCheckIn**, **BossBattleStatus**, **PlayerInventoryItem**, **Reward**

## API Routes

Routers are mounted WITHOUT an `/api/v1` prefix:

| Prefix | Purpose |
|--------|---------|
| `/auth` | Sign in/up/out, refresh session |
| `/users` | User CRUD |
| `/players` | Player profile, XP, level |
| `/profiles` | Profile customization, mood |
| `/subjects` | Subject CRUD |
| `/quests` | Quest CRUD |
| `/study_sessions` | Study session create/end/resume |
| `/tasks` | Task timing sync |
| `/weekly_check_in` | Weekly check-in |
| `/boss_battle_status` | Boss battle flow |
| `/player_inventory_items` | Player inventory / equipped rewards |

## Authentication

- **Access token**: JWT via `Authorization: Bearer <token>` header
- **Refresh token**: HttpOnly, Secure, SameSite=None cookie (`_Host-cramquest_ssfpwrtk`)
- JWT payloads carry both `user_id` and `player_id`; endpoints reject tokens missing either
- Passwords are hashed with bcrypt — never stored in plaintext
