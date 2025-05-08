# NetworkApp Helm Chart

This Helm chart deploys a web application with an Nginx frontend and a backend application, configured with Kubernetes resources including Persistent Volumes, ConfigMaps, Deployments, Services, and an optional Ingress. The chart is designed to be flexible and customizable through Helm values.

## Prerequisites

- Helm 3.x

Kubernetes cluster (version 1.19 or later)

- Access to a container registry for pulling images
- (Optional) Ingress controller (e.g., `ingress-nginx`) for Ingress support

## Installation

1. Clone the repository or download the Helm chart.

2. Navigate to the chart directory:

   ```bash
   cd helm/networkapp
   ```

3. Install the chart using Helm:

   ```bash
   helm install <release-name> . --namespace <namespace> --create-namespace
   ```

   Replace `<release-name>` with your desired release name and `<namespace>` with the target namespace.

## Uninstallation

To uninstall the chart:

```bash
helm uninstall <release-name> --namespace <namespace>
```

## Configuration

The chart is highly configurable via the `values.yaml` file. Below are the key sections and their purposes:

| Parameter | Description | Default |
| --- | --- | --- |
| `global.staticFilesPath` | Shared path for static files | `/app/staticfiles/` |
| `components.nginx.base` | Base name for Nginx resources | `nginx` |
| `components.app.base` | Base name for application resources | `app` |
| `nginx.enabled` | Enable/disable Nginx deployment | `true` |
| `nginx.deployment.replicas` | Number of Nginx replicas | `1` |
| `nginx.container.image` | Nginx container image | `nginx` |
| `nginx.container.tag` | Nginx image tag | `latest` |
| `nginx.container.port` | Nginx container port | `80` |
| `nginx.service.type` | Service type for Nginx | `NodePort` |
| `nginx.service.port` | Nginx service port | `80` |
| `nginx.service.nodePort` | NodePort for Nginx service | `30008` |
| `app.enabled` | Enable/disable application deployment | `true` |
| `app.deployment.replicas` | Number of application replicas | `1` |
| `app.container.image` | Application container image | `nouraldeen152/networkapp` |
| `app.container.tag` | Application image tag | `19` |
| `app.container.port` | Application container port | `8000` |
| `app.service.type` | Service type for application | `ClusterIP` |
| `app.service.port` | Application service port | `8000` |
| `django.env` | Environment variables for Django application | See `values.yaml` |
| `persistence.enabled` | Enable/disable persistent storage | `true` |
| `persistence.capacity` | Storage capacity for PVC | `1Gi` |
| `persistence.accessMode` | Access mode for PV/PVC | `ReadWriteOnce` |
| `persistence.hostPath.path` | Host path for PV (if used) | `/mnt/data` |
| `ingress.enabled` | Enable/disable Ingress | `true` |
| `ingress.className` | Ingress class name | `nginx` |
| `ingress.host` | Hostname for Ingress | `networkapp.local` |
| `ingress.port` | Ingress port | `80` |

### Example: Customizing Values

To override default values, create a custom `values.yaml` or use the `--set` flag:

```bash
helm install my-release . --set nginx.deployment.replicas=2 --set persistence.capacity=5Gi
```

## Resources Created

- **PersistentVolume (PV)**: Provides storage for the application.
- **PersistentVolumeClaim (PVC)**: Requests storage for the Nginx deployment.
- **ConfigMap**: Defines Nginx configuration for routing static files and proxying requests.
- **Deployment (Nginx)**: Runs the Nginx container with mounted volumes for configuration and static files.
- **Service (Nginx)**: Exposes the Nginx deployment, typically via `NodePort`.
- **Deployment (App)**: Runs the backend application container with environment variables.
- **Service (App)**: Exposes the application, typically via `ClusterIP`.
- **Ingress** (Optional): Configures external access to the Nginx service via a specified hostname.

## Accessing the Application

- If `ingress.enabled` is `true`, access the application at `http://<ingress.host>` (e.g., `http://networkapp.local`).
- If using `NodePort`, access the application at `http://<node-ip>:<nodePort>` (default `nodePort: 30008`).
- Ensure the Ingress controller is running if Ingress is enabled, and update DNS or `/etc/hosts` for the Ingress hostname.

## Notes

- The chart supports either `hostPath` or `storageClass` for persistent storage. Uncomment `persistence.storageClass` in `values.yaml` for dynamic provisioning.
- The commented-out `volumeMounts` and `volumes` in the application deployment can be enabled to share the same PVC with Nginx for static files.
- Ensure the `ingress-nginx` controller is installed if `ingress.enabled` is `true`. Use the `ingress-nginx.enabled` field to install it via the chart.

## Upgrading the Chart

To upgrade the chart with new values:

```bash
helm upgrade <release-name> . --namespace <namespace>
```

## Troubleshooting

- Check pod logs: `kubectl logs <pod-name> -n <namespace>`
- Describe resources: `kubectl describe <resource> <name> -n <namespace>`
- Verify Ingress: Ensure the Ingress controller is running and the hostname is resolvable.