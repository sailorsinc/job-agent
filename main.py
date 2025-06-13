from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from playwright.sync_api import sync_playwright
from starlette.concurrency import run_in_threadpool
from agent import react_loop
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def _fetch_job_urls_sync(domain: str):
    start_url = domain
    if not start_url.startswith("http://") and not start_url.startswith("https://"):
        start_url = "https://" + start_url
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            urls, transcript = react_loop(
                page, start_url, "Find links to job postings and list them."
            )
            browser.close()
    except Exception as exc:
        raise RuntimeError(f"Playwright error: {exc}") from exc

    return urls, transcript


async def fetch_job_urls(domain: str):
    return await run_in_threadpool(_fetch_job_urls_sync, domain)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "jobs": [], "logs": []})


@app.post("/fetch", response_class=HTMLResponse)
async def fetch(request: Request, domain: str = Form(...)):
    try:
        jobs, logs = await fetch_job_urls(domain)
        context = {"request": request, "jobs": jobs, "logs": logs}
    except Exception as exc:
        context = {"request": request, "jobs": [], "logs": [], "error": str(exc)}
    return templates.TemplateResponse("index.html", context)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False)
