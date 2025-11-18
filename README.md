git clone https://github.com/bibekkd/fastapi-learning.git
## **FastAPI Learning Project**

A concise, hands-on FastAPI example project demonstrating core concepts: routing, validation, SQLAlchemy models, and user management.

**Quick Highlights**
- **Tech:** `FastAPI`, `SQLAlchemy`, `Pydantic`, `Passlib` (`pbkdf2_sha256`)
- **DB:** PostgreSQL (example uses NeonDB connection in `blog/database.py`)
- **Run:** `uvicorn main:app --reload`

## **Quick Start**
- **Clone:** `git clone https://github.com/bibekkd/fastapi-tut.git`
- **Enter project:** `cd fastapi-tut-one`
- **Activate venv (provided):** `source fastapi-venv/bin/activate`
- **Install deps (if needed):** `pip install -r requirements.txt`
- **Run server:** `uvicorn main:app --reload`
- **API:** `http://127.0.0.1:8000`
- **Docs (Swagger):** `http://127.0.0.1:8000/docs`

## **Project Structure**
- **`main.py`**: application entrypoint, includes the `blog` router and creates DB tables on startup
- **`blog/`**: package containing `models.py`, `routes.py`, `schema.py`, `database.py`
	- **`models.py`**: SQLAlchemy models (`Blog`, `User`)
	- **`routes.py`**: API endpoints (blogs + user creation)
	- **`schema.py`**: Pydantic request/response models
	- **`database.py`**: SQLAlchemy engine & `SessionLocal` configuration

## **Database**
- The example uses a PostgreSQL URL in `blog/database.py` (NeonDB example). On app start, `models.Base.metadata.create_all(bind=engine)` creates tables if they don't exist.
- If your DB user lacks permission to create tables, create them manually or adjust DB privileges.

## **User passwords & security**
- Passwords are hashed using `passlib` with the `pbkdf2_sha256` scheme (no native `bcrypt` dependency required).
- If you need `bcrypt` specifically, install a compatible `bcrypt` wheel in your venv and I can help pin versions.

## **Common Commands**
- Activate venv: `source fastapi-venv/bin/activate`
- Run server: `uvicorn main:app --reload`
- Create DB tables (done automatically at startup) by visiting any endpoint after starting the server.

## **Troubleshooting**
- `ModuleNotFoundError: No module named 'sqlalchemy'` — ensure venv is active and run `pip install -r requirements.txt`.
- `passlib/bcrypt` errors — the repo now uses `pbkdf2_sha256`. To use `bcrypt`, reinstall `bcrypt` and `passlib` with compatible versions.
- `404` on `/` — use `GET /blog` or the documented endpoints; root now includes the router so `GET /` may be absent depending on your routes.

## **Contributing & Notes**
- This repo is for learning. Suggestions and PRs are welcome.
- If you'd like, I can add tests, CI, or Docker setup next.

---
_Maintained as a learning project by bibekkd_