from playwright.sync_api import sync_playwright

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

def fill_form(page):
    try:
        page.fill('input[name="name"]', "John Doe")
        page.fill('input[name="email"]', "john@example.com")
        page.fill('input[name="phone"]', "+1234567890")
        page.set_input_files('input[type="file"]', "resumes/my_resume.pdf")
        return "Form filled."
    except Exception as e:
        return f"Error filling form: {str(e)}"

def submit_form(page):
    try:
        page.click('button[type="submit"]')
        return "Form submitted."
    except Exception as e:
        return f"Error during form submission: {str(e)}"
