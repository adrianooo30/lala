import asyncio
from playwright.async_api import async_playwright
from database import SessionLocal, Inmate

async def scrape_madison():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        print("Navigating to Madison County...")
        try:
            await page.goto("https://www.madisoncountysheriffal.org/inmate-roster", wait_until="networkidle")
            
            # Heuristic wait
            await page.wait_for_timeout(5000)
            inmates = await page.query_selector_all(".inmate-card, table tr")
            
            session = SessionLocal()
            count = 0
            for item in inmates:
                text = await item.inner_text()
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                if not lines: continue
                full_name = lines[0]
                
                if full_name.lower() in ['name', 'inmate', 'inmate name']: continue # Skip header

                img = await item.query_selector("img")
                photo_url = await img.get_attribute("src") if img else ""

                inmate_record = Inmate(
                    county="Madison",
                    full_name=full_name,
                    first_name=full_name,
                    last_name="",
                    photo_url=photo_url,
                    details=text
                )
                session.add(inmate_record)
                count += 1
            session.commit()
            print(f"Scraped {count} inmates from Madison County.")
        except Exception as e:
            print(f"Failed to scrape Madison, could be Cloudflare block. Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_madison())
