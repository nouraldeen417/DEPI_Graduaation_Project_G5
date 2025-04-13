module "network" {
  source = "./modules/network"
  # VPC configuration
  vpc_name               = "main-vpc"
  vpc_cidr               = "10.0.0.0/16"
  vpc_reagion            = "us-east-1"
  public_subnet_count    = 2
  private_subnet_count   = 2
  availability_zones     = ["us-east-1a", "us-east-1b"]
  ngw_tagname            = "ngw"
  igw_tagname            = "igw"
  public_rtable_tagname  = "public-route-table"
  private_rtable_tagname = "private-route-table"
}

module "security" {
  source = "./modules/security"
  # Security group configuration
  vpc_id  = module.network.vpc_id
  sg_name = "allow_ssh_http"

  ingress_rules = [
    {
      from_port   = 22 # SSH
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"] # Warning: Open to the world (restrict in production!)
    },
    {
      from_port   = 80 # HTTP
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  ]
  # Egress rules (outbound traffic) - Added!
  egress_rules = [
    {
      from_port   = 0 # Allow ALL outbound traffic by default
      to_port     = 0
      protocol    = "-1" # All protocols
      cidr_blocks = ["0.0.0.0/0"]
    }
  ]
  # ssh_key_pair = "ssh-key-network-app"
  # ssh_key_path = "."
}

module "compute" {
  source = "./modules/compute"
  # EC2 instance configuration
  ec2_instance = [
    # Instance 1: Public web server
    {
      name               = "web-server",
      ami                = "ami-084568db4383264d4",
      instance_type      = "t2.micro",
      subnet_id          = module.network.public_subnet_ids[0],
      assign_public_ip   = true,                               # <-- Enable public IP
      security_group_ids = [module.security.security_group_id] # Attach SG
      # user_data        = file("./user.sh "),  # Optional user data script
      key_name = "my-key" # Optional SSH key
    }
  ]

}
resource "null_resource" "setup_management" {
  # Trigger only when instance IP changes (ensures it runs after EC2 creation)
  triggers = {
    instance_ip = module.compute.instance_public_ip[0]
  }

  # Upload the script
  provisioner "file" {
    source      = "user.sh"  # In root directory
    destination = "/tmp/setup_management.sh"
    connection {
      type        = "ssh"
      user        = "ubuntu"  # Adjust per AMI
      private_key = file(var.ssh_key_file)  # Path to the SSH key
      host        = module.compute.instance_public_ip[0]
    }
  }

  # Execute the script
  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/setup_management.sh",
      "DEFAULT_USER=ubuntu /tmp/setup_management.sh",  # Hardcode or pass as var
    ]
    connection {
      type        = "ssh"
      user        = "ubuntu"  # Adjust per AMI
      private_key = file(var.ssh_key_file)  # Path to the SSH key
      host        = module.compute.instance_public_ip[0]
    }
  }
  # Write IP to inventory.txt

provisioner "local-exec" {
    # Append IP under [aws_ec2] if section exists, create it if not
    command = <<EOT
                if ! grep -q '[aws_ec2]' ../ansible/hosts; then
                    echo '[aws_ec2]' >> ../ansible/hosts;   
               fi
                sed -i '/^\[aws_ec2\]$/a ${module.compute.instance_public_ip[0]} ansible_user=management ansible_ssh_private_key_file=${var.ssh_key_file}' ../ansible/hosts;

                EOT
  }  
  # Ensure it runs after the EC2 instance is created
  depends_on = [module.compute.instance_ids]
}


