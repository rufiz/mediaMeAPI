from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.main import app
from app.database import get_db, Base


SQLALCHEMY_DATABASE_URL = 'postgresql://{0}:{1}@{2}:{3}/{4}_test'.format(
    settings.database_username,
    settings.database_password,
    settings.database_hostname,
    settings.database_port,
    settings.database_name
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Yield DB function
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
