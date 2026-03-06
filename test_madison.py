import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("Navigating to Madison County...")
        await page.goto("https://www.madisoncountysheriffal.org/inmate-roster", wait_until="networkidle")
        
        html = await page.content()
        with open("madison.html", "w") as f:
            f.write(html)
            
        await page.screenshot(path="madison.png", full_page=True)
        print("Saved madison.html and madison.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
