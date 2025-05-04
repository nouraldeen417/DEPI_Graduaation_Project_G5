## Deploying a Network Application with Kubernetes

This document provides a comprehensive guide for deploying a Python/Django network application using Kubernetes. The application is containerized with Docker, uses Gunicorn as the WSGI server, and includes an Nginx reverse proxy for serving static files. Kubernetes manifests are used to define the application deployment, services, persistent storage, Nginx configuration, and an optional Ingress for external access. A bash script is provided to manage the application of these manifests.

### 1. Overview

The deployment consists of the following Kubernetes resources:

* **Application Deployment and Service:** Deploys the Django application and exposes it internally.
* **Nginx Deployment and Service:** Runs an Nginx reverse proxy to serve static files and forward requests to the application.
* **ConfigMap:** Stores the Nginx configuration.
* **PersistentVolume (PV) and PersistentVolumeClaim (PVC):** Manages storage for static files shared between the application and Nginx.
* **Ingress (Optional):** Provides external access to the application via an Nginx Ingress controller.
* **Bash Script:** Automates the application or deletion of manifests.

The application image (`nouraldeen152/networkapp:latest`) and Nginx image (`nginx:latest`) are used, with static files persisted using a shared volume.

### 2. Prerequisites

* **Kubernetes Cluster:** A running Kubernetes cluster (e.g., Minikube, EKS, kubadmin).

* **kubectl:** Installed and configured to interact with the cluster.

* **Docker Images:**

  * Application image: `nouraldeen152/networkapp:latest` (assumed to be available in a registry).
  * Nginx image: `nginx:latest`.

* **Nginx Ingress Controller:** Required if using the Ingress resource. Install it using:

  ```bash
  kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
  ```

* **Project Structure:**

  ```plaintext
  ├── manifests/
  │   ├── ingress.yaml
  │   ├── app-deployment.yaml
  │   ├── nginx-deployment.yaml
  │   ├── nginx-configmap.yaml
  │   ├── pv-pvc.yaml
  ├── apply-manifests.sh
  ```

* **Static Files:** Ensure the application image collects static files to `/app/djangoapp/staticfiles` (as per the Dockerfile).

### 3. Kubernetes Manifests

The deployment uses five manifests to configure the application and its dependencies.

#### 3.1. Ingress (Optional)

**File:** `ingress.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: networkapp-ingress
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: nginx-reverseproxy-svc
            port:
              number: 80
```

**Explanation:**

* **Purpose:** Routes external HTTP traffic to the Nginx service.
* **IngressClass:** Uses the nginx Ingress controller.
* **Rules:** Forwards all requests (/) to the `nginx-reverseproxy-svc` service on port 80.
* **Usage:** Optional; requires an Nginx Ingress controller in the cluster.
* **Note:** Update the rules section to include a host if domain-based routing is needed.

#### 3.2. Application Deployment and Service

**File:** `app-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: networkapp
  labels:
    app: networkapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: networkapp
  template:
    metadata:
      labels:
        app: networkapp
    spec:
      containers:
      - image: nouraldeen152/networkapp:latest
        name: networkapp
        ports:
        - containerPort: 8000
        env:
          - name: DJANGO_ALLOWED_HOSTS
            value: localhost,127.0.0.1
          - name: DJANGO_TRUSTED_ORIGIN
            value: http://localhost:30008

---
apiVersion: v1
kind: Service
metadata:
  name: networkapp-svc
  labels:
    app: networkapp-svc
spec:
  selector:
    app: networkapp
  ports:
  - port: 8000
    protocol: TCP
    targetPort: 8000
```

**Explanation:**

* **Deployment:**

  * Deploys one replica of the `nouraldeen152/networkapp:latest` image.
  * Exposes port 8000 for Gunicorn.
  * Sets environment variables for Django (`DJANGO_ALLOWED_HOSTS`, `DJANGO_TRUSTED_ORIGIN`).
* **Service:**

  * Exposes the application internally on port 8000.
  * Uses a ClusterIP service (default type, as NodePort is commented out).

#### 3.3. Nginx Deployment and Service

**File:** `nginx-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-static
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx-reverseproxy
  template:
    metadata:
      labels:
        app: nginx-reverseproxy
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
        volumeMounts:
        - name: nginx-config
          mountPath: /etc/nginx/conf.d
          readOnly: true
        - name: shared-storage
          mountPath: /app/staticfiles/
      volumes:
      - name: nginx-config
        configMap:
          name: nginx-config
      - name: shared-storage
        persistentVolumeClaim:
          claimName: my-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-reverseproxy-svc
spec:
  selector:
    app: nginx-reverseproxy
  type: NodePort
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
    nodePort: 30008
```

**Explanation:**

* **Deployment:**

  * Deploys one replica of the `nginx:latest` image.
  * Exposes port 80 for HTTP traffic.
  * Mounts:

    * A ConfigMap (`nginx-config`) to `/etc/nginx/conf.d` for Nginx configuration.
    * A PVC (`my-pvc`) to `/app/staticfiles/` for serving static files.
* **Service:**

  * Exposes Nginx externally via NodePort on port 30008.
  * Forwards traffic to port 80 on the Nginx pods.

#### 3.4. Nginx ConfigMap

**File:** `nginx-configmap.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
data:
  nginx.conf: |-
    server {
        listen 80;
        server_name 192.168.1.150;

        # Serve static files
        location /static/ {
            alias /app/staticfiles/;
        }

        # Serve media files
        location /media/ {
            alias /app/media/;
        }

        # Forward all other requests to Gunicorn
        location / {
            proxy_pass http://networkapp-svc:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
```

**Explanation:**

* **Purpose:** Stores the Nginx configuration as a ConfigMap.
* **Configuration:**

  * Listens on port 80.
  * Serves static files from `/app/staticfiles/` at `/static/`.
  * Serves media files from `/app/media/` at `/media/`.
  * Proxies all other requests to the `networkapp-svc` service on port 8000.

#### 3.5. PersistentVolume and PersistentVolumeClaim

**File:** `pv-pvc.yaml`

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /mnt/data
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

**Explanation:**

* **PersistentVolume (PV):**

  * Defines a 1Gi storage volume using hostPath at `/mnt/data`.
  * Supports ReadWriteOnce access mode (single node read/write).
* **PersistentVolumeClaim (PVC):**

  * Requests 1Gi of storage with ReadWriteOnce access.
  * Binds to the `my-pv` PV.

### 4. Bash Script for Managing Manifests

**File:** `apply-manifests.sh`

```bash
#!/bin/bash

# Directory containing Kubernetes manifest files
MANIFESTS_DIR="$(pwd)/manifests"

# Check if the directory exists
if [ ! -d "$MANIFESTS_DIR" ]; then
  echo "Error: Directory $MANIFESTS_DIR not found."
  exit 1
fi

# Validate the mode argument
if [ "$1" != "apply" ] && [ "$1" != "delete" ]; then
  echo "Usage: $0 <apply|delete>"
  exit 1
fi

MODE=$1

# Apply all YAML files in the directory
for FILE in "$MANIFESTS_DIR"/*.yaml "$MANIFESTS_DIR"/*.yml; do
  if [ -f "$FILE" ]; then
    echo "Applying manifest: $FILE"
    kubectl "$MODE" -f "$FILE" --kubeconfig=${KUBECONFIG}
    if [ $? -ne 0 ]; then
      echo "Error: Failed to $MODE $FILE"
      exit 1
    fi
  fi
done

echo "All manifests $MODE ed successfully."
```

**Explanation:**

* **Purpose:** Automates applying or deleting Kubernetes manifests.
* **Logic:**

  * Checks for the manifests directory.
  * Validates the input argument (`apply` or `delete`).
  * Iterates through `.yaml` and `.yml` files in the manifests directory.
  * Runs `kubectl apply` or `kubectl delete` for each file.
  * Uses the `KUBECONFIG` environment variable for cluster authentication.

### 5. Deployment Instructions

#### Prepare the Cluster:

* Ensure `kubectl` is configured with the correct `KUBECONFIG`.
* If using Ingress, install the Nginx Ingress controller.

#### Organize Manifests:

* Place all manifest files (`ingress.yaml`, `app-deployment.yaml`, `nginx-deployment.yaml`, `nginx-configmap.yaml`, `pv-pvc.yaml`) in the `manifests/` directory.
* Place the bash script (`apply-manifests.sh`) in the project root.

#### Apply Manifests:

```bash
export KUBECONFIG=~/.kube/config
./apply-manifests.sh apply
```

#### Access the Application:

* **Without Ingress:** Use the Nginx NodePort service:

  ```bash
  minikube ip  # Get the cluster IP (for Minikube)
  curl http://<cluster-ip>:30008
  ```
* **With Ingress:** Configure a domain or use the Ingress controller's IP:

  ```bash
  kubectl get ingress networkapp-ingress
  curl http://<ingress-ip>
  ```

#### Verify Deployments:

```bash
kubectl get pods
kubectl get svc
kubectl get ingress
```

### 6. Best Practices

* **Storage:** Replace hostPath with a production-grade storage class. Ensure the application writes static files to the PVC if mounted.
* **Ingress:** Configure a proper domain and TLS for production. Update `DJANGO_ALLOWED_HOSTS` and `DJANGO_TRUSTED_ORIGIN` to match the Ingress domain.
* **Scaling:** Increase replicas in deployments for high availability. Use Horizontal Pod Autoscaling for dynamic scaling.

### 7. Troubleshooting

* **Pod Failures:** Check pod logs:

  ```bash
  kubectl logs -l app=networkapp
  kubectl logs -l app=nginx-reverseproxy
  ```
* **Service Connectivity:** Verify service endpoints:

  ```bash
  kubectl describe svc networkapp-svc
  kubectl describe svc nginx-reverseproxy-svc
  ```
* **Ingress Issues:** Ensure the Ingress controller is running and check Ingress status:

  ```bash
  kubectl get ingress networkapp-ingress -o yaml
  ```
* **Storage Issues:** Verify PV/PVC binding:

  ```bash
  kubectl describe pv my-pv
  kubectl describe pvc my-pvc
  ```
* **Nginx Configuration:** Test the ConfigMap:
