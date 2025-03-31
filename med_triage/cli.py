import click
import uvicorn
from pathlib import Path
import subprocess
import sys
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from datetime import datetime

from .db.database import SessionLocal
from .models.message import Message
from .core.classifier import MessageClassifier

load_dotenv()

@click.group()
def cli():
    """Healthcare Inbox Triage Application CLI"""
    pass

@cli.command()
@click.option('--host', default='127.0.0.1', help='Host to run the API server on')
@click.option('--port', default=8000, help='Port to run the API server on')
def run_api(host, port):
    """Run the FastAPI backend server"""
    uvicorn.run("med_triage.api.main:app", host=host, port=port, reload=True)

@cli.command()
@click.option('--host', default='127.0.0.1', help='Host to run the dashboard on')
@click.option('--port', default=8050, help='Port to run the dashboard on')
def run_dashboard(host, port):
    """Run the Dash dashboard"""
    subprocess.run([sys.executable, "-m", "med_triage.dashboard.app"], env={
        **os.environ,
        "DASH_HOST": host,
        "DASH_PORT": str(port)
    })

@cli.command()
@click.argument('csv_file', type=click.Path(exists=True))
def process_messages(csv_file):
    """Process messages from a CSV file"""
    import pandas as pd
    
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Initialize the classifier
    classifier = MessageClassifier()
    
    # Initialize database session
    db = SessionLocal()
    processed_count = 0
    
    try:
        for _, row in df.iterrows():
            # Classify the message
            category, confidence, explanation = classifier.classify_message(
                row['subject'],
                row['message']
            )
            
            # Create message object
            message = Message(
                message_id=row['message_id'],
                subject=row['subject'],
                content=row['message'],
                datetime=datetime.fromisoformat(row['datetime']),
                triage_category=category,
                confidence_score=confidence,
                notes=explanation
            )
            
            # Add to database
            db.add(message)
            processed_count += 1
            
            # Commit every 10 messages to avoid memory issues
            if processed_count % 10 == 0:
                db.commit()
                click.echo(f"Processed {processed_count} messages...")
        
        # Final commit
        db.commit()
        click.echo(f"Successfully processed {processed_count} messages")
        
    except Exception as e:
        db.rollback()
        click.echo(f"Error processing messages: {str(e)}", err=True)
    finally:
        db.close()

@cli.command()
def init_db():
    """Initialize the database"""
    from med_triage.db.database import engine
    from med_triage.models.message import Base
    
    Base.metadata.create_all(bind=engine)
    click.echo("Database initialized successfully")

def main():
    cli()

if __name__ == '__main__':
    main() 