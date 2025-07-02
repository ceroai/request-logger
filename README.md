# Request Logging API

This is a simple API built with FastAPI that logs the details of every incoming HTTP request. It is designed to be deployed as a serverless container on Google Cloud Run.

## Features

- **Catch-all Endpoint**: Captures all requests (GET, POST, PUT, DELETE, etc.) to any URL path.
- **Structured Logging**: Logs the following information for each request in JSON format to standard output:
  - URL
  - HTTP Method
  - Source IP Address (`X-Forwarded-For` header or remote address)
  - Request Payload (Body)
  - Request Headers
- **Containerized**: Includes a `Dockerfile` for easy building and deployment.
- **Fast Dependencies**: Uses `uv` for fast Python package management.

## How it Works

The application uses a FastAPI middleware to intercept every request before it hits the endpoint. The middleware extracts the relevant information, formats it into a JSON object, and prints it to the console. Cloud Run automatically collects these logs, allowing you to view them in the Google Cloud Logging interface.

The main endpoint simply returns a `200 OK` response with the message "Request logged".

## Deployment to Google Cloud Run

(Instructions will be provided separately)
