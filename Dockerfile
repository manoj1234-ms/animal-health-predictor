
# ---------------------------------------------------
# VetNet AI Backend Dockerfile
# ---------------------------------------------------
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    pandas \
    numpy \
    scikit-learn \
    xgboost \
    torch --index-url https://download.pytorch.org/whl/cpu \
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
