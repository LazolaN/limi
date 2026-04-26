FROM python:3.12-slim
WORKDIR /app

# Ensure /app is on sys.path for alembic + scripts (uvicorn picks it up via cwd,
# but installed-script entry points like `alembic` and `python scripts/...` need this).
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
