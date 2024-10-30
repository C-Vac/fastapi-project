from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

from config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://settings.database_username:password123@localhost:5432/fastapi"


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Absolutely fuck the database
def nuke_database():
    print("Nuking the database...")
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    with engine.begin() as conn:
        for table_name in table_names:
            conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))

    push_model_updates()
    print("Database nuked! All tables deleted and regenerated.")


def push_model_updates():
    from .models import Base

    Base.metadata.create_all(bind=engine)
    print("Updated table models were pushed to the database.")
