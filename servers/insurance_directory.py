import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "insurance_directory.db"

_seed_doctors = [
    ("Dr. John Smith",       "neumology",            "john.smith@city-hospital.com"),
    ("Dr. Jane Doe",         "neumology",            "jane.doe@metro-clinic.com"),
    ("Dr. Robert Johnson",   "digestive",            "robert.johnson@central-hospital.com"),
    ("Dr. Alice Williams",   "ophthalmology",        "alice.williams@eye-care-center.com"),
    ("Dr. Katia O'Hara",     "allergist",            "katia.ohara@eye-care-center.com"),
    ("Dr. Peter Parker",     "cardiologist",         "peter.parker@new-hospital.com"),
    ("Dr. Alaitz Martinez",  "neurologist",          "alaitz.martinez@new-hospital.com"),
    ("Dr. Fatima Panisello", "general_practitioner", "fatima.panisello@new-hospital.com"),
]


def init_db(db_path: Path = DB_PATH) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                name      TEXT NOT NULL,
                speciality TEXT NOT NULL,
                email     TEXT NOT NULL UNIQUE
            )
        """)
        conn.commit()


def seed_doctors(db_path: Path = DB_PATH) -> None:
    with sqlite3.connect(db_path) as conn:
        if conn.execute("SELECT COUNT(*) FROM doctors").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO doctors (name, speciality, email) VALUES (?, ?, ?)",
                _seed_doctors,
            )
            conn.commit()
            print(f"Seeded {len(_seed_doctors)} doctors into {db_path}")
        else:
            print(f"Table already contains data — skipping seed")


if __name__ == "__main__":
    init_db()
    seed_doctors()
