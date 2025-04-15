#!/bin/bash

# Create the management user with home directory and Bash shell
sudo useradd -m -s /bin/bash management

# Grant passwordless sudo privileges
sudo bash -c 'echo "management ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/management'
sudo chmod 440 /etc/sudoers.d/management

# Set up SSH directory and copy authorized_keys from the default user
sudo mkdir -p /home/management/.ssh
sudo cp "/home/ubuntu/.ssh/authorized_keys" /home/management/.ssh/authorized_keys
# Set ownership and permissions
sudo chown -R management:management /home/management/.ssh
sudo chmod 700 /home/management/.ssh
sudo chmod 600 /home/management/.ssh/authorized_keys 
sudo echo "done creating management user with passwordless sudo and SSH access"