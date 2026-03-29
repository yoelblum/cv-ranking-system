import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "cv_database.db"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS candidates (
                id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                phone TEXT,
                title TEXT,
                years_experience INTEGER,
                skills TEXT,
                summary TEXT,
                previous_experience TEXT
            )
            """
        )


def wipe_and_insert(records: list[dict]) -> int:
    with _connect() as conn:
        conn.execute("DELETE FROM candidates")
        conn.executemany(
            """
            INSERT INTO candidates
                (id, name, email, phone, title, years_experience, skills, summary, previous_experience)
            VALUES
                (:id, :name, :email, :phone, :title, :years_experience, :skills, :summary, :previous_experience)
            """,
            [
                {
                    **r,
                    "skills": json.dumps(r["skills"]) if isinstance(r["skills"], list) else r["skills"],
                }
                for r in records
            ],
        )
    return len(records)


def get_all_candidates() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM candidates").fetchall()
    results = []
    for row in rows:
        d = dict(row)
        try:
            d["skills"] = json.loads(d["skills"])
        except (json.JSONDecodeError, TypeError):
            d["skills"] = []
        results.append(d)
    return results
