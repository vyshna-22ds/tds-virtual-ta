FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    wget && \
    pip install --upgrade pip

# Install precompiled faiss-cpu from pypi
RUN pip install faiss-cpu

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install other Python dependencies
RUN pip install -r requirements.txt

# Expose port for FastAPI
EXPOSE 8000

# Start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
