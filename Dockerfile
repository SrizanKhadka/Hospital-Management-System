# Use an official Python runtime as the base image
FROM python:3.12.1
# FROM specifies the base image to build on; here, we’re using Python version 3.12.1. This means our container will have Python pre-installed.

# Set environment variables to prevent Python from creating .pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE 1
# PYTHONDONTWRITEBYTECODE=1 prevents Python from writing .pyc files, which are compiled files, and aren’t necessary here.
ENV PYTHONBUFFERED 1
# PYTHONBUFFERED=1 tells Python to print output directly, without buffering. This helps you see logs in real-time.

# Set the working directory inside the container
WORKDIR /app
# WORKDIR sets "/app" as the main directory inside the container, where we’ll place our app files. 

# Copy and install dependencies from requirements.txt
COPY requirements.txt /app/
# COPY copies "requirements.txt" from our machine into "/app" in the container.
RUN pip install --no-cache-dir -r requirements.txt
# RUN runs commands in the container during the build. Here, it installs all dependencies from "requirements.txt".
# --no-cache-dir ensures pip doesn’t cache packages, reducing image size.

# Copy all Django project files into the container
COPY . /app/
# This COPY command copies everything from our local project folder into "/app" in the container.

# Expose port 8000 to allow access to the Django app
EXPOSE 8000
# EXPOSE makes port 8000 available outside the container. Django’s default port is 8000, so this lets us access the app.

# Run the Django development server
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
# CMD specifies the command to start the app when the container runs. Here, it starts Django's development server on port 8000 and listens on all IP addresses (0.0.0.0) so we can access it externally.
