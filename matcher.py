import os
from thefuzz import fuzz, process
from database import SessionLocal, Inmate, Match
from email_notifier import send_match_alert

def find_matches_in_db(extracted_names: list[str], pdf_filename: str, context: str = ""):
    session = SessionLocal()
    inmates = session.query(Inmate).all()
    inmate_db_names = {inmate.full_name.upper(): inmate for inmate in inmates}
    
    matches_found = []
    
    for ename in extracted_names:
        ename_upper = ename.upper()
        
        if not inmate_db_names:
            continue
            
        best_match = process.extractOne(ename_upper, list(inmate_db_names.keys()), scorer=fuzz.token_sort_ratio)
        if best_match:
            matched_str, score = best_match
            # Empirical threshold for fuzzy matching names
            if score >= 75: 
                matched_inmate = inmate_db_names[matched_str]
                
                # Check if we already logged this match
                existing_match = session.query(Match).filter_by(
                    inmate_id=matched_inmate.id,
                    pdf_filename=pdf_filename
                ).first()
                
                if not existing_match:
                    new_match = Match(
                        inmate_id=matched_inmate.id,
                        pdf_filename=pdf_filename,
                        extracted_name=ename,
                        confidence_score=float(score),
                        match_context=context
                    )
                    session.add(new_match)
                    session.commit()
                    
                    # Refresh object to get it fully detached if needed, or keep it
                    session.refresh(new_match)
                    matches_found.append(new_match)
                    
                    print(f"Match found! PDF Name: {ename} -> DB Name: {matched_inmate.full_name} (Score: {score})")
                    # Trigger email alert
                    send_match_alert(matched_inmate.full_name, pdf_filename)
                else:
                    matches_found.append(existing_match)
                
    return matches_found

if __name__ == "__main__":
    pass
