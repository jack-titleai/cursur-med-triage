from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import pandas as pd

from ..db.database import get_db
from ..models.message import Message
from ..core.classifier import MessageClassifier

app = FastAPI(title="Healthcare Inbox Triage API")
classifier = MessageClassifier()

@app.get("/")
async def root():
    return {"message": "Healthcare Inbox Triage API"}

@app.post("/messages/process")
async def process_messages(file_path: str, db: Session = Depends(get_db)):
    """Process messages from a CSV file and classify them."""
    try:
        df = pd.read_csv(file_path)
        processed_count = 0
        
        for _, row in df.iterrows():
            category, confidence, explanation = classifier.classify_message(
                row['subject'],
                row['message']
            )
            
            message = Message(
                message_id=row['message_id'],
                subject=row['subject'],
                content=row['message'],
                datetime=datetime.fromisoformat(row['datetime']),
                triage_category=category,
                confidence_score=confidence,
                notes=explanation
            )
            
            db.add(message)
            processed_count += 1
            
        db.commit()
        return {"message": f"Processed {processed_count} messages successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/messages")
async def get_messages(
    category: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get messages with optional filtering."""
    query = db.query(Message)
    
    if category:
        query = query.filter(Message.triage_category == category)
    if start_date:
        query = query.filter(Message.datetime >= start_date)
    if end_date:
        query = query.filter(Message.datetime <= end_date)
        
    messages = query.all()
    return messages

@app.put("/messages/{message_id}")
async def update_message(
    message_id: str,
    category: Optional[str] = None,
    notes: Optional[str] = None,
    is_read: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Update a message's classification or status."""
    message = db.query(Message).filter(Message.message_id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
        
    if category:
        message.triage_category = category
    if notes:
        message.notes = notes
    if is_read is not None:
        message.is_read = is_read
        
    db.commit()
    return message

@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get statistics about message classifications."""
    total = db.query(Message).count()
    categories = db.query(Message.triage_category).distinct().all()
    
    stats = {
        "total_messages": total,
        "categories": {}
    }
    
    for category in categories:
        category = category[0]
        count = db.query(Message).filter(Message.triage_category == category).count()
        stats["categories"][category] = count
        
    return stats 