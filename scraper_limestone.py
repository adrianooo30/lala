import asyncio
import json
from playwright.async_api import async_playwright
from database import SessionLocal, Inmate

async def intercept_response(response):
    # Depending on SPA, it might be a JSON response with inmate data
    if "inmates" in response.url and response.status == 200:
        try:
            data = await response.json()
            # If we intercept JSON we can parse it directly
        except:
            pass

async def scrape_limestone():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        print("Navigating to Limestone County...")
        try:
            await page.goto("https://limestone-al-911.zuercherportal.com/#/inmates", wait_until="networkidle")
            
            # Since this is a SPA, wait for cards to render
            await page.wait_for_timeout(5000) 
            
            # Simple fallback selector
            cards = await page.query_selector_all(".inmate-card, .list-group-item, tr")
            session = SessionLocal()
            count = 0
            for card in cards:
                text = await card.inner_text()
                if not text or "Name" not in text: continue
                lines = [l.strip() for l in text.split('\n') if l.strip()]
                full_name = lines[0] # heuristic
                
                img = await card.query_selector("img")
                photo_url = await img.get_attribute("src") if img else ""
                
                inmate = Inmate(
                    county="Limestone",
                    full_name=full_name,
                    first_name=full_name,
                    last_name="",
                    photo_url=photo_url,
                    details=text
                )
                session.add(inmate)
                count += 1
            session.commit()
            print(f"Scraped {count} inmates from Limestone County.")
        except Exception as e:
            print(f"Failed to scrape Limestone: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_limestone())
