# Campus Event Management System

Small Flask backend + static frontend for managing campus events. 
This project was built as a learning-focused full-stack web application to explore Flask, databases, and role-based access.


## Repo layout

- `Backend/` — Flask backend, models, routes, and migrations
- `Frontend/` — HTML/CSS/JS static frontend
- `requirements.txt` — Python dependencies

## Quick start (Windows PowerShell)

1. Create and activate a virtual environment

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Optional: configure environment variables

- `DATABASE_URL` — SQLAlchemy database URL (example using SQLite):

```powershell
$env:DATABASE_URL = "sqlite:///Backend/instance/app.db"
```

- `SECRET_KEY` — Flask secret key (optional):

```powershell
$env:SECRET_KEY = "your-secret-key"
```

If you don't set `DATABASE_URL`, configure one before running the app.

4. Run the backend

```powershell
python Backend/app.py
```

The backend starts on the configured Flask port (default during development). 
On first run, database tables are initialized. 
Test users may be created depending on the local configuration.

5. Open the frontend

- Visit: `http://127.0.0.1:8000/index.html`

The backend serves static frontend files and poster images from the project structure.

## Database migrations

This project includes Flask-Migrate. Typical migration workflow:

```bash
# set DATABASE_URL if needed
flask db init     # (only if migrations not initialized locally)
flask db migrate -m "message"
flask db upgrade
```

Note: `app.py` already initializes the DB on startup via `db.create_all()`.

## Git / push tips

A minimal workflow to push to GitHub:

```bash
git init
git add .
git commit -m "Initial commit"
# create a repo on GitHub and then:
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

## Security & next steps

- Replace `SECRET_KEY` with a secure value for production.
- Use a real database server (MySQL/Postgres) for production and set `DATABASE_URL` accordingly.
- Review `Backend/static/posters/` and `Frontend/Images/` before committing large media files — consider using Git LFS or hosting images externally.

If you want, I can also:
- Create a GitHub Actions workflow for tests/CI
- Prepare a .gitattributes or add Git LFS config for large images
- Commit these files and create the initial repo for you
