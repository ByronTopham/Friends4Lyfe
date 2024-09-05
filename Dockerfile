# Use the appropriate base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies including sqlite3
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

# Copy the necessary files into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code into the container
COPY . .

# Create directories and set permissions
RUN mkdir -p /app/db && chmod -R 755 /app/db
RUN mkdir -p /app/static && chmod -R 777 /app/static

# Set environment variables
ENV FLASK_APP=app/main.py

# Expose the port the Flask app runs on
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run", "--host", "0.0.0.0"]
