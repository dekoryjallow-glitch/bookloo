# Backend Dockerfile

# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (required for OpenCV/cv2 and others)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (FastAPI default)
EXPOSE 8000

# Run the application
# Use shell form to allow variable expansion if needed, but array form is safer.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
