variable "vpc_id" {
  type        = string
  description = "provide a vpc id"
}

variable "sg_name" {
  description = "Name of the security group"
  type        = string
  default     = "allow_ssh_http"
}

variable "ingress_rules" {
  description = "List of inbound rules (ports, protocols, CIDRs)"
  type = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
  }))
  default = [
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
}

# Egress rules (outbound traffic) - Added!
variable "egress_rules" {
  description = "List of outbound rules (ports, protocols, CIDRs)"
  type = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
  }))
  default = [
    {
      from_port   = 0 # Allow ALL outbound traffic by default
      to_port     = 0
      protocol    = "-1" # All protocols
      cidr_blocks = ["0.0.0.0/0"]
    }
  ]
}
# SSH Variables  
variable "ssh_key_pair" {
  type        = string
  default     = "ssh-key-pair"
  description = "provide a key name for the ssh key"
}
variable "ssh_key_path" {
  type        = string
  default     = "."
  description = "provide a key path for the ssh key"
}