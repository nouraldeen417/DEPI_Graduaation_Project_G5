# Docker Images for a Network Application and Docker Compose Deployment

This guide outlines how to containerize and deploy a Django-based network application using Docker, Gunicorn, and an optional custom Nginx reverse proxy. It also demonstrates how to orchestrate these services using Docker Compose.

---

## 1. Overview

This deployment consists of two main Docker images:

* **Application Image**: A Python-based container running a Django application with Gunicorn as the WSGI server.
* **Nginx Image (Optional)**: A custom Nginx container acting as a reverse proxy and static file server.

Docker Compose manages service orchestration, networking, and shared volumes for static files.

---

## 2. Prerequisites

* **Docker**: Ensure Docker is installed and running.

* **Docker Compose**: Required to orchestrate multi-container setups.

* **Project Structure**:

  ```
  ├── djangoapp/
  │   ├── manage.py
  │   ├── staticfiles/
  │   └── storefront/
  │       └── wsgi.py
  ├── requirements.txt
  ├── Dockerfile
  ├── nginx.conf
  └── docker-compose.yml
  ```

* `requirements.txt`: Includes Python dependencies (e.g., `django`, `gunicorn`, `ansible`).

* `nginx.conf`: Custom Nginx configuration for reverse proxy (if used).

---

## 3. Docker Image for the Django Application

**Dockerfile (Dockerfile.app)**

```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt \
    && python djangoapp/manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "storefront.wsgi:application"]
```

**Build the Image**

```bash
docker build -f Dockerfile.app -t nouraldeen152/networkapp:${BUILD_NUMBER} .
```

Replace `${BUILD_NUMBER}` with your version (e.g., `1.0`).

---

## 4. Docker Image for Nginx (Optional)

**Dockerfile (Dockerfile.nginx)**

```dockerfile
FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**nginx.conf**

```nginx
server {
    listen 80;
    server_name localhost;

    location /static/ {
        alias /app/staticfiles/;
    }

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**Build the Image**

```bash
docker build -f Dockerfile.nginx -t nouraldeen152/nginx_reverse_proxy:${BUILD_NUMBER} .
```

---

## 5. Docker Compose Configuration

**docker-compose.yml**

```yaml
version: '3.8'

services:
  web:
    image: nouraldeen152/networkapp:${BUILD_NUMBER}
    ports:
      - "8000:8000"
    volumes:
      - staticfiles:/app/djangoapp/staticfiles
    environment:
      - DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,${HOST_IP}
      - DJANGO_TRUSTED_ORIGIN=http://localhost,http://${HOST_IP}

  nginx:
    image: nouraldeen152/nginx_reverse_proxy:${BUILD_NUMBER}
    ports:
      - "80:80"
    volumes:
      - staticfiles:/app/staticfiles
    depends_on:
      - web

volumes:
  staticfiles:
```

**Run the Application**

```bash
export BUILD_NUMBER=1.0
docker-compose up -d
```

* **Without Nginx**: Visit `http://localhost:8000`
* **With Nginx**: Visit `http://localhost`

---

## 6. Best Practices

* **.dockerignore**: Exclude files like `__pycache__`, `.git`, and `*.pyc` to reduce image size.
* **STATIC\_ROOT**: Set in Django settings to `/app/djangoapp/staticfiles`.
* **Environment Variables**: Use a `.env` file and `env_file:` in Compose to manage secrets.
* **Logging**: Configure Gunicorn and Nginx for logging and debugging.

---

## 7. Troubleshooting

* **Port Conflicts**: Ensure ports 80/8000 are free.
* **Missing Static Files**: Check `collectstatic` ran and `STATIC_ROOT` matches volume path.
* **Nginx Proxy Issues**: Inspect logs via `docker logs <nginx-container>`.
* **Django Errors**: Ensure `DJANGO_ALLOWED_HOSTS` includes all necessary hosts/IPs.

---

## 8. Conclusion

This Docker-based deployment offers a scalable, modular, and production-ready setup for Django applications. Docker Compose simplifies orchestration, while Gunicorn and optional Nginx provide efficient application and static file serving.

For advanced configurations, consult the official [Docker](https://docs.docker.com/), [Django](https://docs.djangoproject.com/), [Gunicorn](https://docs.gunicorn.org/), and [Nginx](https://nginx.org/en/docs/) documentation.

---
