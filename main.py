from fastapi import File, UploadFile, Form

@app.post("/apply")
async def apply_job(url: str = Form(...), file: UploadFile = File(...)):
    from playwright.async_api import async_playwright
    import os

    # Save the uploaded file temporarily
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url, timeout=60000)
            await page.wait_for_load_state("networkidle")

            # Add logic to interact with the job site, e.g., fill form with resume if needed

            await browser.close()
        return {"status": "success", "resume_saved_as": file_location}
    except Exception as e:
        return {"status": "error", "message": str(e)}
