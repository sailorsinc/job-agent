from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from playwright.sync_api import sync_playwright
from agent import react_loop
from tools import gather_job_postings
import uvicorn
import os
import json

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


class FetchRequest(BaseModel):
    url: str


@app.post("/fetch_jobs")
async def fetch_jobs(req: FetchRequest):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        jobs = gather_job_postings(page, req.url)
        browser.close()
    return {"jobs": jobs}


@app.post("/apply_to_job")
async def apply_to_job(job_id: int = Form(...), file: UploadFile = File(...)):
    index_path = "job_postings/index.json"
    if not os.path.exists(index_path):
        return {"error": "No job postings fetched."}
    with open(index_path, "r", encoding="utf-8") as f:
        index = json.load(f)
    job = next((j for j in index if j["id"] == job_id), None)
    if not job:
        return {"error": "Invalid job id."}

    resume_path = f"resumes/{file.filename}"
    with open(resume_path, "wb") as out_file:
        out_file.write(await file.read())

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        react_loop(page, job["url"], "Apply to the given job posting", resume_path)
        browser.close()

    os.remove(resume_path)
    return {"status": "application submitted"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False)
