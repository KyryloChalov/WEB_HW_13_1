from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from src.database.models import Base
from src.conf.config import settings
from static.colors import GRAY, RESET


def reset_db():
    Base.metadata.drop_all(engine, checkfirst=True)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine


def check_tables():

    def table_list(existing_tables) -> str:
        if existing_tables:
            result = "Tables already exist in the database:"
            for table_name in existing_tables:
                result = result + "\n\t- " + table_name
        else:
            result = "There is no table in the database"
        return result

    # Отримуємо список всіх таблиць (якщо вони є в бд)
    tables_metadata = MetaData()
    tables_metadata.reflect(bind=engine)
    existing_tables = tables_metadata.tables.keys()

    # print(" >>>", GRAY, table_list(existing_tables), RESET) # for debugging
    if not existing_tables:
        reset_db()
        print(" >>>", GRAY, table_list(existing_tables), RESET)  # for debugging


SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)

check_tables()


SessionLocal = sessionmaker(
    expire_on_commit=True, autocommit=False, autoflush=False, bind=engine
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
