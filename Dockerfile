FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/processed logs

# Initialize database
RUN python -c "from src.models import init_database; init_database('data/normas_aps.db')"

# Expose port for web portal
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=src.portal.app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/stats')" || exit 1

# Default command - run web portal
CMD ["python", "-m", "src.portal.app"]
