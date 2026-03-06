import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("Navigating to Limestone County...")
        # Since it's a SPA, we wait for networkidle
        await page.goto("https://limestone-al-911.zuercherportal.com/#/inmates", wait_until="networkidle")
        
        html = await page.content()
        with open("limestone.html", "w") as f:
            f.write(html)
            
        await page.screenshot(path="limestone.png", full_page=True)
        print("Saved limestone.html and limestone.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
