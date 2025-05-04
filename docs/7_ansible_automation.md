# Ansible-Based Deployment of a Network Application

This repository provides an automated deployment process for a Python/Django network application using Ansible, Docker, and Docker Compose on CentOS and Debian servers. It supports both on-premises and AWS environments and integrates with Terraform for AWS provisioning.

---

## 1. Overview

This Ansible setup automates:

- **Environment Preparation**: Installs Docker and configures the system.
- **Application Deployment**: Copies `docker-compose.yml` and runs the application using Docker Compose.

### Components

- **Inventory**:  
  - `inventory/aws_inventory.yml` – AWS EC2 instances (compatible with Terraform)  
  - `inventory/onprem_inventory.yml` – On-premises servers  
- **Roles**:  
  - `docker_install`: Installs Docker and configures services.  
  - `docker_compose`: Deploys the application using Docker Compose.  
- **Main Playbook**: `site.yml` applies the appropriate roles.


---

## 2. Prerequisites

- **Control Node**:
  - Ansible installed (`pip install ansible`)
- **Target Hosts**:
  - CentOS or Debian servers with SSH access (preferably key-based)
- **Optional**:
  - Terraform (for provisioning AWS EC2 instances)

---

## 3. Project Structure

```

.
├── inventory/
│   ├── aws\_inventory.yml
│   ├── onprem\_inventory.yml
├── roles/
│   ├── docker\_install/
│   │   └── tasks/
│   │       └── main.yml
│   ├── docker\_compose/
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   └── files/
│   │       └── docker-compose.yml
├── site.yml

````

---

## 4. Ansible Configuration

### 4.1. Main Playbook

**File**: `site.yml`

```yaml
- name: Apply selected roles
  hosts: all
  become: yes
  become_method: sudo
  vars:
    ansible_ssh_common_args: '-o StrictHostKeyChecking=accept-new'
  roles:
    - { role: docker_install, when: "'docker_install' in selected_roles" }
    - { role: docker_compose, when: "'docker_compose' in selected_roles" }
````

> Run:
> `ansible-playbook -i inventory/aws_inventory.yml site.yml -e "selected_roles=['docker_install','docker_compose'] IMAGE_TAG=20"`

---

### 4.2. Docker Install Role

**File**: `roles/docker_install/tasks/main.yml`

```yaml
# Debian/Ubuntu
- name: Add Docker GPG key
  apt_key:
    url: https://download.docker.com/linux/ubuntu/gpg
    state: present
  when: ansible_os_family == "Debian"

- name: Add Docker repository
  apt_repository:
    repo: "deb [arch=amd64] https://download.docker.com/linux/ubuntu {{ ansible_distribution_release }} stable"
    state: present
    update_cache: yes
  when: ansible_os_family == "Debian"

- name: Install Docker
  apt:
    name: "{{ docker_packages }}"
    state: present
  when: ansible_os_family == "Debian"

# CentOS
- name: Add Docker repo
  yum_repository:
    name: docker-ce
    baseurl: https://download.docker.com/linux/centos/$releasever/$basearch/stable
    gpgkey: https://download.docker.com/linux/centos/gpg
    gpgcheck: yes
    enabled: yes
  when: ansible_os_family == "RedHat"

- name: Install Docker
  dnf:
    name: "{{ docker_packages }}"
    state: present
  when: ansible_os_family == "RedHat"

# Common
- name: Ensure Docker service is running
  service:
    name: docker
    state: started
    enabled: yes

- name: Add user to docker group
  user:
    name: "{{ ansible_user_id }}"
    groups: docker
    append: yes
```

**Variables** (`roles/docker_install/defaults/main.yml`):

```yaml
docker_packages:
  - docker-ce
  - docker-ce-cli
  - containerd.io
  - docker-compose-plugin
```

---

### 4.3. Docker Compose Role

**File**: `roles/docker_compose/tasks/main.yml`

```yaml
- name: Get ansible user home directory
  set_fact:
    ansible_home: "{{ ansible_env.HOME }}"

- name: Copy docker-compose.yml
  copy:
    src: files/docker-compose.yml
    dest: "{{ ansible_home }}/docker-compose.yml"

- name: Run Docker Compose
  command: docker compose up -d
  args:
    chdir: "{{ ansible_home }}"
  environment:
    BUILD_NUMBER: "{{ IMAGE_TAG }}"
    HOST_IP: "{{ ansible_host }}"
```

---

### 4.4. Docker Compose File

**File**: `roles/docker_compose/files/docker-compose.yml`

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
    image: nouraldeen152/nginx-reverse-proxy:${BUILD_NUMBER}
    ports:
      - "80:80"
    volumes:
      - staticfiles:/app/staticfiles
    depends_on:
      - web

volumes:
  staticfiles:
```

---

## 5. Deployment Instructions

### Prepare Inventory

* Add public IPs to `aws_inventory.yml` or on-prem IPs to `onprem_inventory.yml`.
* Ensure SSH access (key-based preferred).

### Run the Playbook

**AWS**:

```bash
ansible-playbook -i inventory/aws_inventory.yml site.yml -e "selected_roles=['docker_install','docker_compose'] IMAGE_TAG=20"
```

**On-Premises**:

```bash
ansible-playbook -i inventory/onprem_inventory.yml site.yml -e "selected_roles=['docker_install','docker_compose'] IMAGE_TAG=20"
```

---

## 6. Verification

* Access the application:

  * `http://<host-ip>:80` (via Nginx)
  * `http://<host-ip>:8000` (direct to Gunicorn)
* SSH and check containers:

  ```bash
  ssh <user>@<host-ip> "docker ps"
  ```

---

## 7. Troubleshooting

* **SSH Errors**:

  * Check SSH keys and `ansible_ssh_common_args`
  * Test SSH: `ssh <user>@<host-ip>`
* **Docker Issues**:

  * Validate repo URLs/GPG keys
  * Use verbose mode: `--verbose`
* **Compose Errors**:

  * Pull images manually: `docker pull nouraldeen152/networkapp:20`
  * Validate config: `docker compose config`
* **Port/Access Errors**:

  * Check open ports: `netstat -tuln`
  * View logs: `docker logs <container-id>`

---

## 8. Conclusion

This Ansible-based approach provides a modular, repeatable deployment process for Django-based applications across hybrid infrastructures. It supports secure, scalable deployments with a clear structure and integration with tools like Terraform.

> For production, consider:
>
> * Enhancing security
> * Handling failures gracefully
> * Managing secrets and inventories using Ansible Vault or SSM

---

## References

* [Ansible Documentation](https://docs.ansible.com/)
* [Docker Docs](https://docs.docker.com/)
* [Docker Compose Docs](https://docs.docker.com/compose/)
* [Django Documentation](https://docs.djangoproject.com/)

```

---

Let me know if you'd like this saved as a file or need a downloadable version.
```
