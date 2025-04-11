variable "vpc_name" {
  type        = string
  default     = "main-vpc"
  description = "provide a tag name for the vpc"
}
variable "vpc_cidr" {
  type        = string
  default     = "10.0.0.0/16"
  description = "provide a cidr for the vpc"
}
variable "vpc_reagion" {
  type        = string
  default     = "us-east"
  description = "provide a region for the vpc"
}

variable "public_subnet_1_cidr" {
  type        = string
  default     = "10.0.1.0/24"
  description = "provide a cidr for the public_subnet_1"
}
variable "public_subnet_2_cidr" {
  type        = string
  default     = "10.0.2.0/24"
  description = "provide a cidr for the public_subnet_2"
}

variable "private_subnet_1_cidr" {
  type        = string
  default     = "10.0.3.0/24"
  description = "provide a cidr for the private_subnet_1"
}
variable "private_subnet_2_cidr" {
  type        = string
  default     = "10.0.4.0/24"
  description = "provide a cidr for the private_subnet_2"
}

variable "public_subnet_1_tagname" {
  type        = string
  default     = "public_subnet_1"
  description = "provide a tagname for the public_subnet_1"
}
variable "public_subnet_2_tagname" {
  type        = string
  default     = "public_subnet_2"
  description = "provide a tagname for the public_subnet_2"
}
variable "private_subnet_1_tagname" {
  type        = string
  default     = "private_subnet_1"
  description = "provide a tagname for the private_subnet_1"
}
variable "private_subnet_2_tagname" {
  type        = string
  default     = "private_subnet_2"
  description = "provide a tagname for the private_subnet_2"
}
variable "ssh_key_name" {
  type        = string
  default     = "ssh-key-pair"
  description = "provide a key name for the ssh key"
}
variable "ssh_key_pair" {
  type        = string
  default     = "ssh-key-pair"
  description = "provide a key name for the ssh key"
}
variable "ssh_key_pair_path" {
  type        = string
  default     = "."
  description = "provide a key path for the ssh key"
}
variable "ngw_tagname" {
  type        = string
  default     = "ngw"
  description = "provide a name for nat gateway"
}
variable "igw_tagname" {
  type        = string
  default     = "igw"
  description = "provide a name for nat gateway"
}
variable "public_rtable_tagname" {
  type        = string
  default     = "public-route-table"
  description = "provide a name for public route table"
}
variable "private_rtable_tagname" {
  type        = string
  default     = "private-route-table"
  description = "provide a name for private route table"
}
variable "bastion_tagname" {
  type        = string
  default     = "bastion"
  description = "provide a name for bastion host"
}
variable "bastion_ami" {
  type        = string
  default     = "ami-084568db4383264d4" # Amazon Linux 2 AMI
  description = "provide a ami for bastion host"
}
variable "bastion_instance_type" {
  type        = string
  default     = "t2.micro"
  description = "provide a instance type for bastion host"
}

variable "security_group_name" {
  type        = string
  default     = "allow_ssh"
  description = "allow ssh inbound traffic and all outbound traffic"
}
