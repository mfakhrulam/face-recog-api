# Dockerfile
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY app .

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
