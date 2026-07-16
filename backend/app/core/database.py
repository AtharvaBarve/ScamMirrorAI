from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from app.core.config import settings

# SQLAlchemy setup
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def ensure_sqlite_schema():
    """Add columns required by current models when using an existing SQLite DB."""
    if "sqlite" not in settings.DATABASE_URL:
        return

    required_columns = {
        "category": "VARCHAR(50)",
        "risk_factors": "TEXT",
        "recommended_actions": "TEXT",
        "processing_time": "FLOAT",
        "threat_campaign_id": "INTEGER",
    }

    with engine.begin() as connection:
        existing_rows = connection.execute(text("PRAGMA table_info(analysis_history)")).fetchall()
        existing_columns = {row[1] for row in existing_rows}

        for column_name, column_type in required_columns.items():
            if column_name not in existing_columns:
                connection.execute(
                    text(f"ALTER TABLE analysis_history ADD COLUMN {column_name} {column_type}")
                )

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
