FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY storage.py .
COPY atlas_voice.py .
COPY VERSION .

# Copy static files (needed for iframe mode)
COPY static/ static/

# Create data directory (used by FileStorage fallback)
RUN mkdir -p data

# Railway sets PORT env var; default to 8000
ENV PORT=8000
ENV STORAGE_BACKEND=supabase

EXPOSE ${PORT}

CMD uvicorn app:app --host 0.0.0.0 --port ${PORT}
