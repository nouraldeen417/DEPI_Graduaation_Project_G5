# This file defines the EC2 instances to be created in AWS.
resource "aws_instance" "this" {
  count                  = length(var.ec2_instance) # Creates one instance per list item
  ami                    = var.ec2_instance[count.index].ami
  instance_type          = var.ec2_instance[count.index].instance_type
  subnet_id              = var.ec2_instance[count.index].subnet_id
  vpc_security_group_ids = var.ec2_instance[count.index].security_group_ids
  user_data              = var.ec2_instance[count.index].user_data
  key_name               = var.ec2_instance[count.index].key_name
  # Enable public IP if requested
  associate_public_ip_address = var.ec2_instance[count.index].assign_public_ip
  tags = {
    Name = var.ec2_instance[count.index].name
  }
}
