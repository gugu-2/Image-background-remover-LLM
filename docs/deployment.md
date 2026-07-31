# Deployment Guide

When taking the Background Remover API to production, you need a robust setup to handle multiple concurrent requests and manage system resources efficiently (as AI models can be memory-intensive).

## 1. Deploying with Docker (Recommended)

Docker is the easiest way to deploy this API anywhere (AWS, GCP, DigitalOcean, Heroku, etc.).

We have provided a `Dockerfile` in the root of the project.

### Building the Docker Image

Run this command in the root directory:
```bash
docker build -t bg-remover-api .
```

### Running the Docker Container

Once built, you can run it:
```bash
docker run -d -p 8000:8000 --name bg-api bg-remover-api
```
The API is now running and accessible at `http://localhost:8000`.

## 2. Deploying on a Linux Server (Without Docker)

If you are deploying directly to an Ubuntu or Debian VPS, you should use `Gunicorn` with `Uvicorn` workers for production-grade performance.

1. Clone your project to the server.
2. Set up your Python virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -e .
   ```
3. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```
4. Start the server with Gunicorn:
   ```bash
   gunicorn bg_remover.api:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --timeout 120
   ```
   *Note: `-w 4` specifies 4 worker processes. Adjust this based on your server's CPU cores and RAM. Since the AI model requires memory, do not set this too high on small servers.*

## 3. Cloud Provider Quick-Tips

- **Render / Railway / Heroku**: These Platforms-as-a-Service (PaaS) can automatically build and deploy from the provided `Dockerfile`. Just connect your GitHub repository, choose "Docker" as the deployment method, and expose port 8000.
- **AWS EC2**: Provision an Ubuntu instance, SSH in, install Docker, and run the commands from section 1.
- **AWS ECS / Google Cloud Run**: Push your built Docker image to a container registry (ECR or GCR) and deploy the container directly to these serverless container platforms.
