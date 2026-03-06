from database import SessionLocal, Inmate, init_db

def seed_db():
    init_db()
    session = SessionLocal()
    
    mock_inmates = [
        # From Template A
        {"county": "Madison", "full": "David Ryan Vogt", "first": "David", "last": "Vogt"},
        # From Template B
        {"county": "Madison", "full": "Mya Shy Anne Townsend", "first": "Mya", "last": "Townsend"},
        # From Template C
        {"county": "Limestone", "full": "ADAMS, BOBBY EUGENE", "first": "Bobby", "last": "Adams"},
        {"county": "Limestone", "full": "ADAMS, NATHAN CRAIG", "first": "Nathan", "last": "Adams"},
        {"county": "Limestone", "full": "ALLEN, ALYSA RAQUEL", "first": "Alysa", "last": "Allen"},
        {"county": "Limestone", "full": "ALLEN, KESHAN DARREL", "first": "Keshan", "last": "Allen"},
    ]
    
    for m in mock_inmates:
        existing = session.query(Inmate).filter_by(full_name=m["full"]).first()
        if not existing:
            inmate = Inmate(
                county=m["county"],
                full_name=m["full"],
                first_name=m["first"],
                last_name=m["last"],
                photo_url="", # Mock no photo
                details="Mock data seeded for testing pipeline"
            )
            session.add(inmate)
            
    session.commit()
    print("Database seeded with mock entries from PDFs.")

if __name__ == "__main__":
    seed_db()
