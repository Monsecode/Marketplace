provider "aws" {
  region = "us-east-1"
}

# 1. S3 Bucket Privado y Cifrado
resource "aws_s3_bucket" "marketplace_bucket" {
  bucket = "marketplace-carolina-hermosillo" 
}

resource "aws_s3_bucket_public_access_block" "marketplace_bucket_access" {
  bucket                  = aws_s3_bucket.marketplace_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "marketplace_bucket_encryption" {
  bucket = aws_s3_bucket.marketplace_bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# 2. Declaración de la base de datos RDS
resource "aws_db_instance" "marketplace_db" {
  identifier             = "marketplace-db"
  allocated_storage      = 20
  engine                 = "mysql"
  instance_class         = "db.t4g.micro"
  username               = "admin"
  password               = "kangbts7monse" 
  publicly_accessible    = false
  storage_encrypted      = true
  skip_final_snapshot    = true
}
