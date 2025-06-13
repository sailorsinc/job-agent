# Job Agent FastAPI Service

This repository contains a simple FastAPI application that uses Playwright and OpenAI APIs to fetch job posting links from a website.

## Environment Variable

The service expects the OpenAI API key to be available in the environment:

```bash
export OPENAI_API_KEY=<your-api-key>
```

Without this variable the agent in `agent.py` will be unable to call the OpenAI API.

## Installing Dependencies

Install all Python dependencies using `pip`:

```bash
pip install -r requirements.txt
```

Playwright also requires its browser dependencies to be installed. When running in the provided Docker container these are installed automatically via `playwright install --with-deps`.

## Running on Cloud Run

1. **Build and push the container**

```bash
docker build -t gcr.io/<PROJECT_ID>/job-agent:latest .
docker push gcr.io/<PROJECT_ID>/job-agent:latest
```

2. **Deploy to Cloud Run**

```bash
gcloud run deploy job-agent \
  --image gcr.io/<PROJECT_ID>/job-agent:latest \
  --platform managed \
  --region <REGION> \
  --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY
```

The service listens on port `8080` as defined in `entrypoint.sh` and the Dockerfile.

## Internet Access

Cloud Run instances need outbound internet access to download Python packages from `pypi.org` during build time and to reach `api.openai.com` at runtime. Ensure that these domains are allowed if you are restricting egress traffic.

