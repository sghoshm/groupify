# backend/Dockerfile
# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
# Use --no-cache-dir to avoid storing cache, reducing image size
# Use -r to install from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY app/ ./app

# Command to run the application
# uvicorn is the ASGI server
# app.main:app refers to the FastAPI app instance in app/main.py
# --host 0.0.0.0 makes the server accessible externally (within the Docker network)
# --port 8000 sets the port the application listens on
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
