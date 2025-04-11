output "instance_ids" {
  description = "List of private IPs for created instances"
  value       = aws_instance.this[*].id
}
output "instance_public_ip" {
  description = "List of public IP for created instances"
  value       = aws_instance.this[*].public_ip
}
output "instance_private_ips" {
  description = "List of private IPs for created instances"
  value       = aws_instance.this[*].private_ip
}   