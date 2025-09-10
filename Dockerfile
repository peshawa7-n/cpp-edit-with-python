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
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies: build tools and OpenCV dev libs
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files into container
COPY requirements.txt .
COPY video_editor.cpp .
COPY main.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Compile C++ to a shared library
RUN g++ -shared -fPIC -o video_editor.so video_editor.cpp `pkg-config --cflags --libs opencv4`

# Default command
CMD ["python", "main.py"]
