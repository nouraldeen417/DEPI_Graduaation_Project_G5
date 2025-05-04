
# Django Docker Setup with Gunicorn and Nginx

This guide explains how to Dockerize a Django application, serve it using Gunicorn, and configure Nginx as a reverse proxy. It also covers handling static files and troubleshooting common issues.

---

## Table of Content

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Development Setup](#development-setup)
4. [Production Setup](#production-setup)
   - [Using Gunicorn](#using-gunicorn)
   - [Using Nginx as a Reverse Proxy](#using-nginx-as-a-reverse-proxy)
5. [Handling Static Files](#handling-static-files)
6. [Accessing the Application](#accessing-the-application)
7. [Troubleshooting](#troubleshooting)
8. [References](#references)

---

## Prerequisites

- Docker and Docker Compose installed on your machine.
- A Django project ready for deployment.

---

## Project Structure

```
myproject/
├── djangoapp/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── staticfiles/
├── media/
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── requirements.txt
└── manage.py
```

---

## Development Setup

1. **Build the Docker Image**:
   ```bash
   docker-compose build
   ```

2. **Run the Containers**:
   ```bash
   docker-compose up
   ```

3. **Access the Application**:
   - Open your browser and go to `http://localhost:8000`.

---

## Production Setup

### Using Gunicorn

1. **Update `Dockerfile`**:
   Replace the `CMD` instruction with:
   ```dockerfile
   CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project_name.wsgi:application"]
   ```

2. **Rebuild and Run**:
   ```bash
   docker-compose build
   docker-compose up
   ```

---

### Using Nginx as a Reverse Proxy

1. **Create `nginx.conf`**:
   ```nginx
   server {
       listen 80;
       server_name localhost;

       location /static/ {
           alias /app/staticfiles/;
       }

       location /media/ {
           alias /app/media/;
       }

       location / {
           proxy_pass http://web:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

2. **Update `docker-compose.yml`**:
   Add the Nginx service:
   ```yaml
   version: '3.8'

   services:
     web:
       build: .
       command: gunicorn --bind 0.0.0.0:8000 your_project_name.wsgi:application
       volumes:
         - staticfiles:/app/staticfiles
       expose:
         - "8000"
       depends_on:
         - db

     nginx:
       image: nginx:latest
       ports:
         - "80:80"
       volumes:
         - ./nginx.conf:/etc/nginx/conf.d/default.conf
         - staticfiles:/app/staticfiles
       depends_on:
         - web

     db:
       image: postgres:13
       environment:
         POSTGRES_DB: mydatabase
         POSTGRES_USER: myuser
         POSTGRES_PASSWORD: mypassword
       volumes:
         - postgres_data:/var/lib/postgresql/data/

   volumes:
     postgres_data:
     staticfiles:
   ```

3. **Rebuild and Run**:
   ```bash
   docker-compose build
   docker-compose up
   ```

---

## Handling Static Files

1. **Update `settings.py`**:
   ```python
   STATIC_URL = '/static/'
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

   MEDIA_URL = '/media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
   ```

2. **Collect Static Files**:
   Run the following command inside the `web` container:
   ```bash
   docker-compose exec web python manage.py collectstatic --noinput
   ```

---

## Accessing the Application

- **Development**: Access the app at `http://localhost:8000`.
- **Production**: Access the app at `http://localhost` (via Nginx).

---

## Troubleshooting

### 1. **Static Files Not Loading**
   - Ensure `STATIC_ROOT` and `MEDIA_ROOT` are correctly set in `settings.py`.
   - Verify that `collectstatic` has been run.
   - Check Nginx configuration for correct paths.

### 2. **`web` Hostname Not Resolved**
   - Ensure `web` and `nginx` services are in the same Docker network.
   - Verify that the `web` service is running.

### 3. **Nginx Not Serving Static Files**
   - Ensure the `staticfiles` volume is correctly mounted in both `web` and `nginx` services.
   - Check Nginx logs for errors:
     ```bash
     docker-compose logs nginx
     ```

---

## References

- [Docker Documentation](https://docs.docker.com/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Gunicorn Documentation](https://gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

test application 