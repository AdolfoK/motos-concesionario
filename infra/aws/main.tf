# =============================================================================
# Capa de COMPUTO en AWS: instancia EC2 que ejecuta los contenedores
# (frontend nginx + backend Django) y se conecta a la capa de datos en Azure.
# =============================================================================

# Lee los outputs de la capa de Azure (estado local de infra/azure).
data "terraform_remote_state" "azure" {
  backend = "local"
  config = {
    path = "../azure/terraform.tfstate"
  }
}

# AMI oficial de Ubuntu 22.04 LTS (amd64).
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# VPC y subred por defecto (publica) de la region.
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# --- Par de claves SSH -------------------------------------------------------
resource "aws_key_pair" "this" {
  key_name   = "${var.project_name}-key"
  public_key = var.ssh_public_key
}

# --- Grupo de seguridad (firewall de la instancia) ---------------------------
# Solo 80/443 abiertos a internet; SSH restringido a tu IP.
resource "aws_security_group" "web" {
  name        = "${var.project_name}-sg"
  description = "Permite HTTP/HTTPS publico y SSH restringido"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH (solo mi IP)"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip_cidr]
  }

  ingress {
    description = "SSH desde EC2 Instance Connect (consola web AWS, us-east-1)"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["18.206.107.24/29"]
  }

  egress {
    description = "Todo el trafico de salida"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# --- IP elastica (estable) ---------------------------------------------------
resource "aws_eip" "this" {
  domain = "vpc"
}

# --- Instancia EC2 -----------------------------------------------------------
resource "aws_instance" "app" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = data.aws_subnets.default.ids[0]
  vpc_security_group_ids      = [aws_security_group.web.id]
  key_name                    = aws_key_pair.this.key_name
  associate_public_ip_address = true

  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }

  user_data = templatefile("${path.module}/user_data.sh.tpl", {
    repo_url          = var.repo_url
    repo_branch       = var.repo_branch
    django_secret_key = var.django_secret_key
    allowed_hosts     = "localhost,127.0.0.1,${aws_eip.this.public_ip}"
    pg_database       = data.terraform_remote_state.azure.outputs.pg_database
    pg_user           = data.terraform_remote_state.azure.outputs.pg_admin_user
    pg_password       = var.db_admin_password
    pg_host           = data.terraform_remote_state.azure.outputs.pg_fqdn
    storage_account   = data.terraform_remote_state.azure.outputs.storage_account_name
    storage_key       = data.terraform_remote_state.azure.outputs.storage_account_key
    storage_container = data.terraform_remote_state.azure.outputs.storage_container
    whatsapp_numero   = var.whatsapp_numero
    admin_password    = var.django_admin_password
  })

  tags = {
    Name = "${var.project_name}-app"
  }
}

# Asocia la IP elastica a la instancia.
resource "aws_eip_association" "this" {
  instance_id   = aws_instance.app.id
  allocation_id = aws_eip.this.id
}
