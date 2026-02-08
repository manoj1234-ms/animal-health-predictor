# Veterinary AI System - Docker Deployment
# Base image with Python 3.10 (compatible with PyTorch/TensorFlow)
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
# We create a requirements.txt from the installed packages
# For simplicity, we can also manually list them here if requirements.txt doesn't exist
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports
# 8000: FastAPI
# 8501: Streamlit
EXPOSE 8000
EXPOSE 8501

# Copy script to run both services
COPY start_services.sh .
RUN chmod +x start_services.sh

# Default command
CMD ["./start_services.sh"]
