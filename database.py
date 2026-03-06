import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class Inmate(Base):
    __tablename__ = 'inmates'
    id = Column(Integer, primary_key=True, autoincrement=True)
    county = Column(String(50), nullable=False) # 'Madison' or 'Limestone'
    full_name = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    photo_url = Column(Text)
    details = Column(Text) # JSON string of extra details like age, booking date
    scraped_at = Column(DateTime, default=datetime.utcnow)

class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True, autoincrement=True)
    inmate_id = Column(Integer, ForeignKey('inmates.id'), nullable=False)
    pdf_filename = Column(String(255), nullable=False)
    extracted_name = Column(String(255), nullable=False)
    confidence_score = Column(Float, nullable=False) # e.g. 95.5 from thefuzz
    match_context = Column(Text) # Additional text from the PDF highlighting the match
    created_at = Column(DateTime, default=datetime.utcnow)
    
    inmate = relationship("Inmate")

# Setup SQLite database
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inmates.db')
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
