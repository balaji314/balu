# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt first (for layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Expose app port (adjust if needed)
EXPOSE 5000

# Run the Python app (adjust to your main script)
CMD ["python", "app.py"]
