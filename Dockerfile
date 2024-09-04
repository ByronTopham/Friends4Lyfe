# Use the official Python image based on Ubuntu as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the virtual environment into the container
COPY SRE_Stockulator/.venv ./.venv

# Copy the main.py script into the container
COPY SRE_Stockulator/.venv/main.py .

# Copy the requirements.txt file
COPY requirements.txt ./requirements.txt

# Install dependencies using pip from within the virtual environment
RUN ./.venv/bin/pip install --no-cache-dir --upgrade pip && \
    ./.venv/bin/pip install -r requirements.txt

# Expose the port that the Flask app will run on (default Flask port 5000)
EXPOSE 5000

# Set the environment variable to ensure Flask runs in production mode
ENV FLASK_ENV=production

# Set the Python interpreter to use the virtual environment's Python
ENV PATH="/app/.venv/bin:$PATH"

# Command to run the Flask application
CMD ["python", "main.py"]
