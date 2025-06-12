from playwright.sync_api import sync_playwright
import os
import json
from urllib.parse import urljoin

def goto(page, url):
    page.goto(url, timeout=60000)
    return page.content()

def click_text(page, text):
    try:
        page.get_by_text(text, exact=True).click(timeout=5000)
        return page.content()
    except Exception:
        return f"Could not find clickable text '{text}'"

def extract_job_links(page):
    links = page.query_selector_all("a")
    jobs = []
    for link in links:
        text = link.inner_text().lower()
        href = link.get_attribute("href")
        if href and ("job" in text or "apply" in text):
            jobs.append(f"{text.strip()} → {href}")
    return "\n".join(jobs) if jobs else "No job links found."

def fill_form(page, resume_path="resumes/my_resume.pdf"):
    try:
        page.fill('input[name="name"]', "John Doe")
        page.fill('input[name="email"]', "john@example.com")
        page.fill('input[name="phone"]', "+1234567890")
        if resume_path:
            page.set_input_files('input[type="file"]', resume_path)
        return "Form filled."
    except Exception as e:
        return f"Error filling form: {str(e)}"

def submit_form(page):
    try:
        page.click('button[type="submit"]')
        return "Form submitted."
    except Exception as e:
        return f"Error during form submission: {str(e)}"

def gather_job_postings(page, start_url):
    os.makedirs("job_postings", exist_ok=True)
    index = []
    page.goto(start_url, timeout=60000)
    links = page.query_selector_all("a")
    counter = 1
    for link in links:
        text = link.inner_text().lower()
        href = link.get_attribute("href")
        if href and ("job" in text or "apply" in text):
            job_url = href if href.startswith("http") else urljoin(start_url, href)
            try:
                page.goto(job_url, timeout=60000)
                content = page.inner_text("body")
                file_path = f"job_postings/job_{counter}.txt"
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                index.append({"id": counter, "url": job_url})
                counter += 1
                page.goto(start_url)
            except Exception:
                page.goto(start_url)
                continue
    with open("job_postings/index.json", "w", encoding="utf-8") as f:
        json.dump(index, f)
    return index
