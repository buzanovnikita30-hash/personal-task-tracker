# Personal Task Tracker

Production-like single-user task manager with Kanban-first UX, mobile-first layout, quick-add flow, reminders, comments, and change history.

## Stack

- Django 5
- SQLite by default (PostgreSQL-ready via env)
- HTMX + Alpine.js (lightweight interactivity)
- SortableJS (drag-and-drop board)
- Tailwind CSS (CDN)

## Features

- Kanban board (Inbox, Planned, In Progress, Waiting, Done)
- Quick-add task input always visible
- Task detail panel (desktop) / full-screen modal (mobile)
- Priority, due date/time, tags, filters
- Overdue and Today highlighting
- Comments and activity history in separate sections
- Reminder scheduler management command

## Quick start

### Windows one-click start (recommended)

```bat
run_local.bat
```

Script automatically:

- creates `.venv`
- installs dependencies
- creates `.env`
- runs migrations
- seeds demo tasks
- starts server

### Manual start

1. Create venv and install deps:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

1. Configure env:

```bash
copy .env.example .env
```

1. Run migrations and seed:

```bash
python manage.py migrate
python manage.py seed_demo
```

1. Start app:

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Public link (share with anyone)

1. Make sure `.env` contains:

```env
ALLOWED_HOSTS=127.0.0.1,localhost,.trycloudflare.com
```

1. Run Django:

```bash
python manage.py runserver 127.0.0.1:8000
```

1. In another terminal run:

```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

1. Share the generated `https://...trycloudflare.com` URL.

## Permanent public link (recommended)

For a link that opens for everyone in any browser 24/7, deploy to Render:

1. Push this project to GitHub.
2. Open [Render Dashboard](https://dashboard.render.com/) -> New -> Blueprint.
3. Select your repo. Render will read `render.yaml` automatically.
4. Wait for build to complete.
5. Open generated URL: `https://<your-service>.onrender.com`

### Required envs in Render

- `DEBUG=False`
- `SECRET_KEY=<generated>`
- `ALLOWED_HOSTS=.onrender.com`
- `CSRF_TRUSTED_ORIGINS=https://*.onrender.com`
- `DATABASE_URL=<render postgres url or leave sqlite for demo>`

### Why this is better than tunnel

- Works continuously (not tied to your local PC being on)
- Stable HTTPS URL
- Accessible by anyone from any browser/device
- No local terminal needed after deploy

## Reminders

In development, run reminder worker manually:

```bash
python manage.py run_reminder_worker
```

It marks due reminders as sent and logs activity. In production, execute every minute via scheduler/cron.

## Tests

```bash
python manage.py test
```

## GitHub Pages (static preview)

Workflow file: `.github/workflows/deploy.yml`

- GitHub Pages publishes the `site/` folder.
- This is a static preview only (full Django backend does not run on Pages).

