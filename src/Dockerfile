FROM python:3.12-slim

ENV UV_SYSTEM_PYTHON=1

WORKDIR /app

RUN pip install uv

# Create user first
RUN useradd --create-home --shell /bin/bash app || true

# Change ownership of /app directory to app user
RUN chown -R app:app /app

# Copy dependency
COPY --chown=app:app pyproject.toml uv.lock ./
COPY --chown=app:app pm-buddy.pem ./
COPY --chown=app:app pm_buddy/ ./pm_buddy/

# Install dependencies (cached layer if pyproject.toml/uv.lock unchanged)
RUN uv sync --frozen

# Switch to app user after installing dependencies
USER app

EXPOSE 8088

CMD ["uv", "run", "python", "pm_buddy/main.py", "--port", "8088"]