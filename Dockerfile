
# ---------------------------------------------------
# VetNet AI Backend Dockerfile
# ---------------------------------------------------
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for ML libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements if they exist, or install common ones
# Since we don't have a requirements.txt yet, let's create a minimal environment
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    pandas \
    numpy \
    scikit-learn \
    xgboost \
    torch \
    joblib \
    psutil \
    pydantic \
    requests

# Copy project files
COPY . .

# Set PYTHONPATH to include src
ENV PYTHONPATH=/app

# Expose port and start API
EXPOSE 8002
CMD ["python", "simple_api.py"]
