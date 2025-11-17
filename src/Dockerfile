FROM python:3.12-slim

ENV UV_SYSTEM_PYTHON=1

WORKDIR /app

RUN pip install uv

# Create user first
RUN useradd --create-home --shell /bin/bash app || true

# Change ownership of /app directory to app user
RUN chown -R app:app /app

# Copy dependency files first for better layer caching
COPY --chown=app:app pyproject.toml uv.lock ./

# Switch to app user before installing dependencies
USER app

# Install dependencies (cached layer if pyproject.toml/uv.lock unchanged)
RUN uv sync --frozen

# Copy application files after dependencies are installed
COPY --chown=app:app agent.yaml pm-buddy.pem ./
COPY --chown=app:app pm_buddy/ ./pm_buddy/

EXPOSE 8093

CMD ["uv", "run", "python", "-m", "pm_buddy.main", "--port", "8093"]