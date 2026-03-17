FROM python:3.10-slim

WORKDIR /app

# Install necessary tools for Scraper and Networking
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the API port and the UI port
EXPOSE 8000 7860

# Run the Backend in the background, then launch the UI
CMD python api.py & python app.py