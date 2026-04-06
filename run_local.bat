@echo off
setlocal

if not exist ".venv\Scripts\python.exe" (
  echo [setup] Creating virtual environment...
  python -m venv .venv
)

echo [setup] Installing dependencies...
call ".venv\Scripts\python.exe" -m pip install -r requirements.txt

if not exist ".env" (
  echo [setup] Creating .env from template...
  copy /Y ".env.example" ".env" >nul
)

echo [setup] Running migrations...
call ".venv\Scripts\python.exe" manage.py migrate

echo [setup] Seeding demo data...
call ".venv\Scripts\python.exe" manage.py seed_demo

echo [run] Starting app at http://127.0.0.1:8000
call ".venv\Scripts\python.exe" manage.py runserver
