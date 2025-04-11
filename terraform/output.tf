output "bastion_ip" {
  value       = module.compute.instance_public_ip[0]
  description = "Public IP of the bastion host"

}
