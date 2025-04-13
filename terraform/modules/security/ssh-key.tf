# resource "tls_private_key" "ssh-key" {
#   algorithm = "RSA"
#   rsa_bits  = 4096
# }
# resource "aws_key_pair" "generated_key" {
#   key_name   = var.ssh_key_pair
#   public_key = tls_private_key.ssh-key.public_key_openssh
#   # Save the private key to a file
#   # provisioner "local-exec" {
#   #   command = <<-EOT
#   #     echo '${tls_private_key.ssh-key.private_key_pem}' > ${var.ssh_key_path}/${var.ssh_key_pair}.pem
#   #     chmod 400 ${var.ssh_key_path}/${var.ssh_key_pair}.pem
#   #   EOT
#   # }
# }
