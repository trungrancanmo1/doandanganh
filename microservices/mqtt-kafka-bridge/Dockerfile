# Set up the base environment of python
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy 2 files
# /app/pyproject.toml and /app/poetry.lock
COPY pyproject.toml poetry.lock README.md ./

# Install Poetry
RUN pip install poetry

COPY . .

# Install dependencies
RUN poetry install

# Default command (can be overridden by Docker Compose)
CMD ["poetry", "run", "python", "-m", "local_data_process_service.app"]