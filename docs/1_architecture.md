# 1. Architecture Overview

## 🧱 System Components

The architecture of the Network Management System spans across multiple layers:

### 1. Application Layer
- **Django (Python)**: Web application and REST API for managing devices.
- **Gunicorn**: Production-ready WSGI server to serve Django.
- **NGINX**: Reverse proxy for HTTP requests, static files, and optional SSL termination.

### 2. Automation Layer
- **Ansible (Dual Role)**:
  1. **Inside the App**:
     - Executes network configuration tasks (ping, backup, OSPF, VLANs, etc.)
     - Dynamically called from the Django interface.
  2. **Infrastructure Setup (External)**:
     - Used to install Docker and dependencies on raw servers or EC2.
     - Future plan: install and configure full Kubernetes clusters.

### 3. Containerization
- **Docker**:
  - Separate containers for Django, Gunicorn, and NGINX.
  - Images pushed to private registry.

### 4. Deployment Targets
- **Local Server**: Docker Compose setup for testing/development.
- **Remote Server**: Docker engine running containers directly.
- **AWS EC2**: Dockerized deployment provisioned with Terraform.
- **Kubernetes Cluster**: Application deployed using manifests and Helm.

### 5. CI/CD Integration
- **Jenkins**:
  - Orchestrates the build, push, and deploy process.
  - Parametrized to support different environments.
  - Slack notification integration.

---

## 🔄 Data & Control Flow

```text
[User]
   ↓ (HTTP)
[NGINX] 
   ↓ (WSGI)
[Gunicorn] 
   ↓
[Django App] ←→ [Ansible Runner] ←→ [Network Devices]
