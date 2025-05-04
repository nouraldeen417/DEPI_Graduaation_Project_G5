Ansible-Based Deployment of a Network Application
This document outlines the process of using Ansible to prepare the environment and deploy a Python/Django network application on CentOS and Debian distributions. The setup includes installing Docker, configuring the environment, and deploying the application using Docker Compose. The Ansible inventory is split into AWS and on-premises environments to support different infrastructures, with compatibility for Terraform-managed EC2 instances. Two roles are used: one for installing Docker and another for deploying the application.

1. Overview
The deployment uses Ansible to automate:

Environment Preparation: Installs Docker and configures the system on CentOS and Debian.
Application Deployment: Copies the docker-compose.yml file and deploys the application using Docker Compose.

The Ansible setup includes:

Inventory: Two files (aws_inventory.yml and onprem_inventory.yml) to separate AWS and on-premises hosts.
Roles:
docker_install: Installs Docker and configures the service.
docker_compose: Deploys the application using Docker Compose.


Main Playbook: site.yml applies the selected roles based on user input.

The application uses the Docker images nouraldeen152/networkapp:20 and nouraldeen152/nginx-reverse-proxy:1.0, as defined in the previous Kubernetes documentation.

2. Prerequisites

Ansible: Installed on the control node (e.g., pip install ansible).
Target Hosts: CentOS or Debian servers with SSH access.


Terraform (Optional): For provisioning AWS EC2 instances and updating the AWS inventory.
Project Structure:.
├── inventory/
│   ├── aws_inventory.yml
│   ├── onprem_inventory.yml
├── roles/
│   ├── docker_install/
│   │   ├── tasks/
│   │   │   ├── main.yml
│   ├── docker_compose/
│   │   ├── tasks/
│   │   │   ├── main.yml
│   │   ├── files/
│   │   │   ├── docker-compose.yml
├── site.yml


SSH Access: Ensure the Ansible control node has SSH access to target hosts (key-based authentication recommended).


3. Ansible Inventory
The inventory is split into two files to support AWS and on-premises environments, facilitating Terraform integration for AWS hosts.


4. Ansible Playbook and Roles
4.1. Main Playbook
File: site.yml
- name: Apply selected roles
  hosts: all
  become: yes
  become_method: sudo
  vars:
    ansible_ssh_common_args: '-o StrictHostKeyChecking=accept-new'
  roles:
    - { role: docker_install, when: "'docker_install' in selected_roles" }
    - { role: docker_compose, when: "'docker_compose' in selected_roles" }

Explanation:

Targets all hosts in the inventory.
Uses become: yes to run tasks with sudo.
Automatically accepts new SSH keys to simplify automation.
Conditionally applies roles based on the selected_roles variable.
Usage:ansible-playbook -i inventory/aws_inventory.yml site.yml -e "selected_roles=['docker_install','docker_compose']"



4.2. Docker Install Role
File: roles/docker_install/tasks/main.yml
- name: Add Docker GPG key (Debian/Ubuntu)
  ansible.builtin.apt_key:
    url: https://download.docker.com/linux/ubuntu/gpg
    state: present
  when: ansible_os_family == "Debian"

- name: Add Docker repository (Debian/Ubuntu)
  ansible.builtin.apt_repository:
    repo: "deb [arch=amd64] https://download.docker.com/linux/ubuntu {{ ansible_distribution_release }} stable"
    state: present
    update_cache: yes
  when: ansible_os_family == "Debian"

- name: Install Docker (Debian/Ubuntu)
  ansible.builtin.apt:
    name: "{{ docker_packages }}"
    state: present
  when: ansible_os_family == "Debian"

- name: Add Docker repository (CentOS)
  ansible.builtin.yum_repository:
    name: docker-ce
    description: Docker CE Stable - $basearch
    baseurl: https://download.docker.com/linux/centos/$releasever/$basearch/stable
    gpgcheck: yes
    gpgkey: https://download.docker.com/linux/centos/gpg
    enabled: yes
    state: present
  when: ansible_os_family == "RedHat"

- name: Install Docker (CentOS)
  ansible.builtin.dnf:
    name: "{{ docker_packages }}"
    state: present
  when: ansible_os_family == "RedHat"

- name: Ensure Docker service is started and enabled
  ansible.builtin.service:
    name: docker
    state: started
    enabled: yes

- name: Add user to docker group
  ansible.builtin.user:
    name: "{{ ansible_user_id }}"
    groups: docker
    append: yes

Explanation:

Debian/Ubuntu Tasks:
Adds the Docker GPG key.
Configures the Docker repository for the specific release.
Installs Docker packages (defined in docker_packages).


CentOS Tasks:
Adds the Docker repository for CentOS.
Installs Docker using dnf.


Common Tasks:
Starts and enables the Docker service.
Adds the Ansible user to the docker group for non-root access.


Variables:
docker_packages: Define in roles/docker_install/defaults/main.yml:docker_packages:
  - docker-ce
  - docker-ce-cli
  - containerd.io
  - docker-compose-plugin





4.3. Docker Compose Role
File: roles/docker_compose/tasks/main.yml
- name: Get ansible user home directory
  ansible.builtin.set_fact:
    ansible_home: "{{ ansible_env.HOME }}"

- name: Copy docker-compose.yml to home directory
  ansible.builtin.copy:
    src: files/docker-compose.yml
    dest: "{{ ansible_home }}/docker-compose.yml"

- name: Run Docker Compose from home directory
  ansible.builtin.command: "docker compose up -d"
  args:
    chdir: "{{ ansible_home }}"
  environment:
    BUILD_NUMBER: "{{ IMAGE_TAG }}"
    HOST_IP: "{{ ansible_host }}"

Explanation:

Determines the user's home directory.
Copies docker-compose.yml from roles/docker_compose/files/ to the home directory.
Runs docker compose up -d with environment variables BUILD_NUMBER and HOST_IP.
Variables:
IMAGE_TAG: Specifies the image tag (e.g., 20).
ansible_host: The target's IP address.



4.4. Docker Compose File
File: roles/docker_compose/files/docker-compose.yml
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

Explanation:

Defines two services: web (Django/Gunicorn) and nginx (reverse proxy).
Uses images with the BUILD_NUMBER tag (e.g., 20).
Shares static files via a staticfiles volume.
Configures Django environment variables using HOST_IP.


5. Deployment Instructions

Prepare the Inventory:

Update aws_inventory.yml with EC2 public IPs (manually or via Terraform).
Update onprem_inventory.yml with on-premises server IPs.
Ensure SSH keys are accessible.


Set Up Ansible:

Install Ansible: pip install ansible.
Create the project structure and place files as described.


Run the Playbook:

For AWS:ansible-playbook -i inventory/aws_inventory.yml site.yml -e "selected_roles=['docker_install','docker_compose'] IMAGE_TAG=20"


For on-premises:ansible-playbook -i inventory/onprem_inventory.yml site.yml -e "selected_roles=['docker_install','docker_compose'] IMAGE_TAG=20"




Verify Deployment:

Access the application:curl http://<host-ip>:80  # Via Nginx
curl http://<host-ip>:8000  # Direct to Gunicorn


Check Docker containers:ssh <user>@<host-ip> "docker ps"





6. Troubleshooting

SSH Connection Issues:
Verify SSH keys and ansible_ssh_common_args.
Check firewall settings: ssh <user>@<host-ip>.


Docker Installation Failures:
Check repository URLs and GPG keys.
View Ansible logs: ansible-playbook ... --verbose.


Docker Compose Errors:
Ensure images are available: docker pull nouraldeen152/networkapp:20.
Verify docker-compose.yml syntax: docker compose config.


Application Access:
Confirm ports 80 and 8000 are open: netstat -tuln.
Check container logs: docker logs <container-id>.




7. Conclusion
This Ansible setup automates the preparation and deployment of a Django network application on CentOS and Debian, supporting both AWS and on-premises environments. The split inventory facilitates Terraform integration, while the docker_install and docker_compose roles ensure consistent environment setup and application deployment. For production, enhance security, error handling, and inventory management based on the best practices outlined.
For further details, refer to the official Ansible, Docker, Docker Compose, and Django documentation.
