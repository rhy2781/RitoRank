variable "aws_region"{
  type = string
}

variable "aws_access_key"{
  type = string
}

variable "aws_secret_key"{
  type = string
}

provider "aws" {
  region = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

resource "aws_s3_bucket" "rito-athena-output"{
  tags = {
     power-rankings-hackathon = 2023
  }
}

