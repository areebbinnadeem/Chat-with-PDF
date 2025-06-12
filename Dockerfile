# Stage 1: Builder
FROM python:3.10-slim AS builder

WORKDIR /app

# Install system dependencies with cleanup
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt && \
    find /root/.local -type d -name '__pycache__' -exec rm -rf {} + && \
    find /root/.local -type d -name 'tests' -exec rm -rf {} + && \
    rm -rf /tmp/*

# Stage 2: Runtime
FROM python:3.10-slim

WORKDIR /app

# Copy only what's needed
COPY --from=builder /root/.local /root/.local
COPY . .

# Set environment
ENV PATH=/root/.local/bin:$PATH \
    STREAMLIT_SERVER_PORT=8501 \
    PYTHONUNBUFFERED=1

CMD ["streamlit", "run", "app.py"]