FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget curl unzip fonts-liberation libnss3 libxss1 libasound2 \
    libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 \
    && apt-get clean

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps

RUN chmod +x entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["./entrypoint.sh"]
