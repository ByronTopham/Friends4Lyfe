# Use the official Python image based on Ubuntu as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the virtual environment and main.py script into the container
COPY Friends4Lyfe/SRE_Stockulator/.venv ./.venv
COPY Friends4Lyfe/SRE_Stockulator/main.py .

# Install the Flask package
RUN pip install flask

# Expose the port that the Flask app will run on (default Flask port 5000)
EXPOSE 5000

# Set the environment variable to ensure Flask runs in production mode
ENV FLASK_ENV=production

# Set the Python interpreter to use the virtual environment's Python
ENV PATH="/app/.venv/bin:$PATH"

# Command to run the Flask application
# Replace "main.py" with the correct file name and ensure "main.py" includes app.run()
CMD ["python", "main.py"]
