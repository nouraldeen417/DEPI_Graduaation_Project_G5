#!/bin/bash
# ansible-playbook site.yml -e "selected_roles='docker_install'"
                if ! grep -q '[aws_ec2]' ../ansible/hosts; then
                    echo '[aws_ec2]' >> ../ansible/hosts;   
               fi
                sed -i '/^\[aws_ec2\]$/a ${module.compute.instance_public_ip[0]} ansible_user=management ansible_ssh_private_key_file=${module.security.ssh_key_pair_path}' ../ansible/hosts;

