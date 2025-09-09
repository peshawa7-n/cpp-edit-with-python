# Base image with Python and build tools
FROM python:3.11-slim

# Install g++ for compiling C++ code
RUN apt-get update && apt-get install -y g++ && apt-get clean

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Compile the C++ shared library
RUN g++ -shared -fPIC -o mycpp.so mycpp.cpp

# Run the Python app
CMD ["python", "main.py"]
