# ---------- BUILD STAGE ----------
FROM python:3.13-slim AS builder

WORKDIR /app

RUN apt-get update
RUN apt-get install -y curl build-essential
RUN rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get install -y nodejs
RUN npm install -g npm
RUN rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY static/ ./static/
COPY templates/ ./templates/
COPY package.json package-lock.json ./

RUN npm ci
RUN npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify

# ---------- FINAL STAGE ----------
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY --from=builder /app/src ./src
COPY --from=builder /app/static ./static
COPY --from=builder /app/templates ./templates

# Expose port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
