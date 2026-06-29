output "public_ip" {
  description = "IP publica de la instancia."
  value       = aws_eip.this.public_ip
}

output "app_url" {
  description = "URL de la aplicacion (HTTP)."
  value       = "http://${aws_eip.this.public_ip}"
}

output "ssh_command" {
  description = "Comando para conectarte por SSH."
  value       = "ssh ubuntu@${aws_eip.this.public_ip}"
}
