# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install uv package manager
RUN pip install uv

# Copy project files
COPY . .

# Install dependencies using uv
RUN uv sync --frozen

# Expose the port that the app runs on
EXPOSE 8000

# Run the FastAPI application using uvicorn
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
