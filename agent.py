from openai import OpenAI
import time
from tools import goto, click_text, extract_job_links, fill_form, submit_form
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_gpt(messages):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.3,
    )
    return response.choices[0].message.content

def react_loop(page, start_url, goal, resume_path="resumes/my_resume.pdf"):
    messages = [
        {"role": "system", "content": (
            "You are a job link extraction assistant. "
            "Use tools like goto(url), click(text), and extract_job_links(). "
            "After each observation decide the next step using Thought and Action."
        )},
        {"role": "user", "content": f"Task: {goal}\nStart from: {start_url}"}
    ]

    obs = goto(page, start_url)

    for _ in range(15):
        messages.append({"role": "user", "content": f"Observation: {obs}"})
        reply = call_gpt(messages)
        print("GPT Reply:\n", reply)

        messages.append({"role": "assistant", "content": reply})

        if "Action:" not in reply:
            print("No action found. Exiting.")
            break

        try:
            action_line = [line for line in reply.splitlines() if line.strip().startswith("Action:")][0]
            action = action_line.replace("Action:", "").strip()

            if action.startswith("goto("):
                url = action[5:-1].strip('"')
                obs = goto(page, url)
            elif action.startswith("click("):
                text = action[6:-1].strip('"')
                obs = click_text(page, text)
            elif action.startswith("extract_job_links"):
                obs = extract_job_links(page)
            elif action.startswith("fill_form"):
                obs = fill_form(page, resume_path)
            elif action.startswith("submit_form"):
                obs = submit_form(page)
            else:
                obs = f"Unknown action: {action}"
        except Exception as e:
            obs = f"Error during action execution: {str(e)}"
            print(obs)

        time.sleep(1)

    print("Agent loop finished.")
    return obs
