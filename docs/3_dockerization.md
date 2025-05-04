Docker Images for a Network Application and Docker compose file
This document outlines the process of creating and deploying a Dockerized network application using Python, Gunicorn, and an optional Nginx reverse proxy image custom. The application is containerized using Docker, with dependencies installed via a requirements.txt file, and deployed using Docker Compose for orchestration.

1. Overview
The setup consists of two Docker images:

Application Image: A Python-based image that runs a Django application using Gunicorn as the WSGI server.
Nginx Image (Optional): A custom Nginx image configured as a reverse proxy to serve static files and forward requests to the Gunicorn server.

Docker Compose is used to orchestrate the services, manage networking, and share static files between the application and Nginx containers.

2. Prerequisites

Docker: Ensure Docker is installed and running.
Docker Compose: Ensure Docker Compose is installed.
Project Structure: The application should have the following structure:.
├── djangoapp/
│   ├── manage.py
│   ├── staticfiles/
│   └── storefront/
│       └── wsgi.py
├── requirements.txt
├── Dockerfile
├── nginx.conf
└── docker-compose.yml


requirements.txt: Lists all Python dependencies (e.g., django, gunicorn,ansible).
nginx.conf: Custom Nginx configuration for the reverse proxy (if using Nginx).


3. Docker Image for the Application
The application image is built using a Dockerfile that sets up a Python environment, installs dependencies, collects static files, and runs the Django application with Gunicorn.
Dockerfile for the Application
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY . .

# Install any needed packages specified in requirements.txt and generate static files 
RUN pip install --no-cache-dir -r requirements.txt \
    && python djangoapp/manage.py collectstatic --noinput

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Run Gunicorn directly in the Docker image
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "storefront.wsgi:application"]

Explanation

Base Image: python:3.11-slim provides a lightweight Python 3.11 environment.
Environment Variables:
PYTHONDONTWRITEBYTECODE=1: Prevents Python from writing .pyc files.
PYTHONUNBUFFERED=1: Ensures Python output is sent directly to the terminal.


Working Directory: /app is set as the working directory for the container.
Copy Files: The entire project directory is copied into /app. Ensure only necessary files are included to reduce image size (e.g., use .dockerignore to exclude unnecessary files).
Install Dependencies: pip install installs packages listed in requirements.txt without caching to reduce image size.
Collect Static Files: python djangoapp/manage.py collectstatic --noinput collects Django static files to /app/djangoapp/staticfiles.
Expose Port: Port 8000 is exposed for Gunicorn.
Command: gunicorn runs the Django application, binding to 0.0.0.0:8000.

Building the Application Image

Save the above as Dockerfile.app.
Build the image:docker build -f Dockerfile.app -t nouraldeen152/networkapp:${BUILD_NUMBER} .

Replace ${BUILD_NUMBER} with a version number (e.g., 1.0).


4. Docker Image for Nginx (Optional)
The Nginx image is built to serve static files and act as a reverse proxy, forwarding requests to the Gunicorn server.
Dockerfile for Nginx
# Use the latest official Nginx image
FROM nginx:latest

# Remove the default NGINX configuration file (optional)
RUN rm /etc/nginx/conf.d/default.conf

# Copy your custom configuration file into the container
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 (optional, as NGINX already exposes it)
EXPOSE 80

# Start NGINX in the foreground
CMD ["nginx", "-g", "daemon off;"]

Nginx Configuration File (nginx.conf)
server {
    listen 80;
    server_name localhost;

    # Serve static files
    location /static/ {
        alias /app/staticfiles/;
    }

    # Proxy requests to Gunicorn
    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

Explanation

Base Image: nginx:latest provides a stable Nginx server.
Remove Default Config: The default Nginx configuration is removed to avoid conflicts.
Custom Config: nginx.conf is copied to /etc/nginx/conf.d/default.conf.
Expose Port: Port 80 is exposed for HTTP traffic.
Command: nginx -g "daemon off;" runs Nginx in the foreground.
Nginx Configuration:
Serves static files from /app/staticfiles/ at the /static/ URL.
Proxies all other requests to the web service (Gunicorn) on port 8000.



Building the Nginx Image

Save the Nginx Dockerfile as Dockerfile.nginx.
Save the Nginx configuration as nginx.conf.
Build the image:docker build -f Dockerfile.nginx -t nouraldeen152/nginx_reverse_proxy:${BUILD_NUMBER} .

Replace ${BUILD_NUMBER} with a version number (e.g., 1.0).


5. Docker Compose Configuration
Docker Compose orchestrates the application and Nginx services, ensuring they communicate and share static files via a shared volume.
Docker Compose File (docker-compose.yml)
version: '3.8'

services:
  web:
    image: nouraldeen152/networkapp:${BUILD_NUMBER}
    ports:
      - "8000:8000"
    volumes:
      - staticfiles:/app/djangoapp/staticfiles  # Mount staticfiles volume
    environment:
      - DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,${HOST_IP}
      - DJANGO_TRUSTED_ORIGIN=http://localhost,http://${HOST_IP}

  nginx:
    image: nouraldeen152/nginx_reverse_proxy:${BUILD_NUMBER}
    ports:
      - "80:80"
    volumes:
      - staticfiles:/app/staticfiles  # Mount staticfiles volume
    depends_on:
      - web

volumes:
  staticfiles:

Explanation

Version: Uses Docker Compose version 3.8 for compatibility.
Services:
web: Runs the application image, exposing port 8000 for direct access (optional if using Nginx).
Volumes: Mounts the staticfiles volume to persist and share static files.
Environment: Sets Django settings for allowed hosts and trusted origins required for application to run 
successfully.


nginx: Runs the Nginx image, exposing port 80 for HTTP traffic.
Volumes: Mounts the same staticfiles volume to serve static files.
depends_on: Ensures the web service starts before Nginx.




Volumes: Defines a staticfiles volume to share static files between containers.

Running the Application

Set the BUILD_NUMBER environment variables:export BUILD_NUMBER=1.0


Run Docker Compose:docker-compose up -d


Access the application:
Without Nginx: http://localhost:8000 or http://${HOST_IP}:8000.
With Nginx: http://localhost or http://${HOST_IP}.




6. Best Practices

.dockerignore: Create a .dockerignore file to exclude unnecessary files (e.g., __pycache__, .git, *.pyc) from the Docker image to reduce size.

Static Files: Verify that STATIC_ROOT in Django settings is set to /app/djangoapp/staticfiles.
Environment Variables: Store sensitive data (e.g., DJANGO_SECRET_KEY) in a .env file and load it using env_file in Docker Compose.
Logging: Configure Gunicorn and Nginx logging for debugging.


7. Troubleshooting

Port Conflicts: Ensure ports 80 and 8000 are not in use by other services.
Static Files Not Found: Verify that collectstatic ran successfully and that STATIC_ROOT matches the volume path.
Nginx Proxy Issues: Check the Nginx logs (docker logs <nginx-container>) for errors in the configuration or connectivity to the web service.
Django Settings: Ensure DJANGO_ALLOWED_HOSTS includes the correct hostnames or IPs.


8. Conclusion
This setup provides a scalable and production-ready deployment for a Django application using Docker. The application image handles the backend logic, while the optional Nginx image serves static files and acts as a reverse proxy. Docker Compose simplifies orchestration, making it easy to deploy and manage the services.
For further customization, refer to the official Docker, Django, Gunicorn, and Nginx documentation.
