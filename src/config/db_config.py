import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASS"),
    "database": os.getenv("POSTGRES_DB"),
    "port": os.getenv("POSTGRES_PORT")
}

required_keys = ["host", "user", "password", "database", "port"]
missing_keys = [key for key in required_keys if not DB_CONFIG.get(key)]

if missing_keys:
    raise ValueError(
        f"Missing required database config for: {', '.join(missing_keys)}. "
        "Please check your .env file or environment variables."
    )

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print("Connect DB successfully!")
    except Exception as e:
        print(f"Error when connect to DB: {str(e)}")
