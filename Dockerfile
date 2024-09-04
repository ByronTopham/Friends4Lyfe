# Use the appropriate base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies including sqlite3
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

# Copy the necessary files into the container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code into the container
COPY . .

# Expose the port the Flask app runs on
EXPOSE 5000

RUN mkdir -p /app/db && chmod -R 755 /app/db

ENV FLASK_APP=SRE_Stockulator/.venv/main.py

CMD ["flask", "run", "--host", "0.0.0.0"]
