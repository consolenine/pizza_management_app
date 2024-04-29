from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from api.config.settings import DATABASE_URL

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

Base = declarative_base()

def get_session() -> sessionmaker:
    """
    Returns a new session instance.
    """
    # Create a session class
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Return a new session instance
    return SessionLocal()