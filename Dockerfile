
# ---------------------------------------------------
# VetNet AI Backend Dockerfile
# ---------------------------------------------------
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (excluding PyTorch)
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    pandas \
    numpy \
    scikit-learn \
    xgboost \
    joblib \
    psutil \
    pydantic \
    requests

# Install PyTorch CPU-only version separately
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Copy project files
COPY . .

# Set PYTHONPATH to include src
ENV PYTHONPATH=/app

# Expose port and start API
EXPOSE 8002
CMD ["python", "simple_api.py"]
