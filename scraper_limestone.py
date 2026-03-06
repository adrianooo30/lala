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
            
            # Wait precisely for the inmate table to render
            print("Waiting for the inmate table to render...")
            await page.wait_for_selector("table.table.table-striped-tbody tbody.row-group", timeout=30000)
            
            session = SessionLocal()
            total_count = 0
            
            while True:
                # Additional small timeout to ensure all rows finish rendering
                await page.wait_for_timeout(2000)
                
                tbodies = await page.query_selector_all("table.table.table-striped-tbody tbody.row-group")
                page_count: int = 0
                for tbody in tbodies:
                    name_cell = await tbody.query_selector("td[ordered-tag='name']")
                    if not name_cell:
                        continue
                    
                    full_name = await name_cell.inner_text()
                    full_name = full_name.strip()
                    if not full_name:
                        continue
                        
                    parts = full_name.split(',', 1)
                    last_name = parts[0].strip() if len(parts) > 0 else ""
                    first_name = parts[1].strip() if len(parts) > 1 else full_name
                    
                    img = await tbody.query_selector("td[ordered-tag='mugshot'] img")
                    photo_url = await img.get_attribute("src") if img else ""
                    
                    text = await tbody.inner_text()
                    
                    # See if inmate exists to prevent exact duplicates (optional, we'll just add for now)
                    inmate = Inmate(
                        county="Limestone",
                        full_name=full_name,
                        first_name=first_name,
                        last_name=last_name,
                        photo_url=photo_url,
                        details=text.strip()
                    )
                    session.add(inmate)
                    page_count += 1
                
                session.commit()
                total_count += page_count  # type: ignore
                
                # Check for "Next" button and verify it's not disabled
                next_btn = await page.query_selector("button[ng-click='nextResults()']:not([disabled])")
                if next_btn:
                    print("Moving to the next page of results...")
                    await next_btn.click()
                    # Wait for the table to refresh
                    await page.wait_for_timeout(3000)
                else:
                    break
                
            print(f"Scraped {total_count} inmates from Limestone County.")
        except Exception as e:
            print(f"Failed to scrape Limestone: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_limestone())
