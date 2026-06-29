terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.60"
    }
  }
}

# Usa las credenciales configuradas con 'aws configure'.
provider "aws" {
  region = var.aws_region
}
