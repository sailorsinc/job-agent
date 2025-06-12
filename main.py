from fastapi import FastAPI, Request
from pydantic import BaseModel
from playwright.sync_api import sync_playwright
from agent import react_loop
import uvicorn

app = FastAPI()

class JobRequest(BaseModel):
    url: str
    goal: str = "Find the careers page and apply to a frontend developer job."

@app.post("/apply")
async def apply_job(req: JobRequest):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        react_loop(page, req.url, req.goal)
        browser.close()
    return {"status": "completed"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False)
