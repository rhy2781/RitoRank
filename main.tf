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

resource "aws_s3_bucket" "athena-output"{
  tags = {
     power-rankings-hackathon = 2023
  }
  force_destroy = true
}


resource "aws_glue_catalog_database" "glue-db"{
  name = "rito-glue-database"
}

resource "aws_glue_crawler" "glue-crawler"{
  database_name = aws_glue_catalog_database.glue-db.name
  name = "rito-glue-crawler"
  role = "arn:aws:iam::782420675586:role/service-role/AWSGlueServiceRole-test"
  
  s3_target{
    path = "s3://power-rankings-dataset-gprhack/athena-ready/"
  }
}

resource "aws_security_group" "ec2-ssh"{
  name_prefix = "ec2-ssh-"
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource  "aws_instance" "ec2"{
  ami = "ami-03a6eaae9938c858c"
  instance_type = "t2.micro"
  key_name = "my-AWS-key"
  vpc_security_group_ids = [aws_security_group.ec2-ssh.id]
  tags = {
    name = "backend-ec2"
    power-rankings-hackathon = 2023
  }
}