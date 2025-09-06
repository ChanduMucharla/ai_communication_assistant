
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "emails.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True)
    sender = Column(String(256))
    subject = Column(String(512))
    body = Column(Text)
    received_at = Column(DateTime, default=datetime.utcnow)
    sentiment = Column(String(16))
    priority = Column(String(16))
    phone = Column(String(128))
    alt_email = Column(String(256))
    product = Column(String(256))
    resolved = Column(Boolean, default=False)

class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True)
    email_id = Column(Integer)
    draft = Column(Text)
    sent = Column(Boolean, default=False)
    sent_at = Column(DateTime, nullable=True)

def init_db():
    Base.metadata.create_all(engine)
