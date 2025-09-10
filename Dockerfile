# # Base image with Python and build tools
# FROM python:3.11-slim

# # Install g++ for compiling C++ code
# RUN apt-get update && apt-get install -y g++ && apt-get clean

# # Set working directory
# WORKDIR /app

# # Copy project files
# COPY . .

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Compile the C++ shared library
# RUN g++ -shared -fPIC -o mycpp.so mycpp.cpp

# # Run the Python app
# CMD ["python", "main.py"]
# Use official Python base image
# Use official Python base image
# Start from the official lightweight Python image
FROM python:3.11-slim

# Set environment variables to avoid Python buffering
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create folders for sessions and downloads
RUN mkdir -p /app/sessions /app/downloads

# Copy project files
COPY . .

# Default command to run the script
CMD ["python", "main.py"]
