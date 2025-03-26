# Set up the base environment of python
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy 2 files
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry install --only main --no-root

# Copy the actual application code
COPY . .

# Default command (can be overridden by Docker Compose)
CMD ["poetry", "run", "python", "-m", "local_data_process_service.app"]
