# Use official Python image
FROM python:3.11-slim

# Set work directory inside container
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Install the package itself
RUN pip install .

# Expose port
EXPOSE 8000

# Run the API with Uvicorn
CMD ["uvicorn", "newsagg.main:app", "--host", "0.0.0.0", "--port", "8000"]
