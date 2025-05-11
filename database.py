from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# SQLite connection
engine = create_engine("sqlite:///storybot.db", echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Story log model
class StoryLog(Base):
    __tablename__ = "story_log"

    id = Column(Integer, primary_key=True, index=True)
    speaker = Column(String, nullable=False)  # e.g., "Narrator", "Gecko"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create the database tables
def init_db():
    Base.metadata.create_all(bind=engine)

