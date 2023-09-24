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

resource "aws_glue_crawler" "crawler"{
  database_name = aws_glue_catalog_database.glue-db.name
  name = "rito-glue-crawler"
  role = "arn:aws:iam::782420675586:role/service-role/AWSGlueServiceRole-test"
  
  s3_target{
    path = "s3://power-rankings-dataset-gprhack/athena-ready/"
  }
}
