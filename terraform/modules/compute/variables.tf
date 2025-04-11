variable ec2_instance {
  description = "List of EC2 instances to create"
  type = list(object({
    name               = string                # Unique name for each instance
    ami                = string                # Custom AMI per instance
    instance_type      = string                # Custom instance type
    subnet_id          = string                # Subnet placement
    assign_public_ip   = optional(bool, false) # Add public IP?
    security_group_ids = list(string)          # List of security group IDs
    user_data          = optional(string, "")  # Optional user data script
    key_name           = optional(string, "")  # Optional SSH key
  }))

}

