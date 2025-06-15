FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y build-essential && \
    pip install --upgrade pip

# Copy code
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 7860

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
