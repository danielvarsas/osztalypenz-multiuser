# Backend Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the outside world
EXPOSE 5000

# Define environment variable
ENV FLASK_ENV=production

# Run the Flask app
CMD ["python", "app.py"]
