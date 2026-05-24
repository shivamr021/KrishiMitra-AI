# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Define an environment variable for the temporary directory.
ENV TEMP_DIR=/tmp

# Copy the requirements file into the container first to leverage Docker cache
COPY requirements.txt .

# Install dependencies from requirements.txt
# NOTE: The URL in requirements.txt for en-core-web-sm has been corrected.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire application context into the container.
# This is a simpler alternative to copying each directory individually.
COPY . .

# Make port 7860 available (standard for Hugging Face Spaces)
EXPOSE 7860

# Use gunicorn with a uvicorn worker for production.
# A single worker is used to minimize memory usage on free tiers.
CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:7860"]
