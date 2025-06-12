from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright
import os

app = FastAPI()

@app.post("/apply")
async def apply_job(request: Request):
    data = await request.json()
    url = data.get("url")
    if not url:
        return JSONResponse(content={"error": "Missing 'url' in request."}, status_code=400)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url, timeout=60000)
            await page.wait_for_load_state("networkidle")

            # Example: Try to find 'Careers' link
            try:
                careers_link = await page.wait_for_selector("text=Careers", timeout=5000)
                await careers_link.click()
                await page.wait_for_load_state("networkidle")
            except:
                pass  # If not found, continue

            content = await page.content()
            await browser.close()
            return {"status": "completed", "page_snippet": content[:500]}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
