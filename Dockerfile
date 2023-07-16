FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the application code to the container at /app
ADD app/ /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Immediately dump log messages to the stream instead of being buffered
ENV PYTHONUNBUFFERED True

# Run the Flask app via gunicorn, and with verbose logging
CMD exec gunicorn --bind :80 --workers 1 --threads 8 --timeout 0 --log-level=debug app:app