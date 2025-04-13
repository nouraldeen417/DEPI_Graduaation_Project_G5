output "security_group_id" {
  description = "ID of the created security group"
  value       = aws_security_group.this.id
}
# output "ssh_key_pair_path" {
#   description = "Path to the SSH key pair"
#   value       = "${var.ssh_key_path}/${var.ssh_key_pair}.pem"
# }
# output "ssh_key_pair_name" {
#   description = "Name of the SSH key pair"
#   value       = aws_key_pair.generated_key.key_name
# }