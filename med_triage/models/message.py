from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Enum, Boolean, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    message_id = Column(String, unique=True)
    subject = Column(String)
    content = Column(String)
    datetime = Column(DateTime)
    triage_category = Column(Enum('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'REFERENCE', name='triage_category'))
    confidence_score = Column(Float)
    processed_at = Column(DateTime, default=func.now())
    is_read = Column(Boolean, default=False)
    notes = Column(String, nullable=True)

    def __repr__(self):
        return f"<Message(message_id='{self.message_id}', subject='{self.subject}', triage_category='{self.triage_category}')>" 