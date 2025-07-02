# Use an official lightweight Python image.
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install dependencies using uv
RUN uv pip install --no-cache --system -r requirements.txt

# Copy the rest of the application's code into the container
COPY . .

# Get the port from the environment variable, default to 8080
ENV PORT=8080

# Command to run the application
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
