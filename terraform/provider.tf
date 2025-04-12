# main.tf
provider "aws" {
  region  = "us-east-1"
  # access_key                  = "test"       # Fake credentials
  # secret_key                  = "test"       # Fake credentials
  # s3_use_path_style           = true # 👈 Critical for LocalStack
  # skip_credentials_validation = true # Bypass AWS credential checks
  # skip_metadata_api_check     = true # Bypass EC2 metadata check
  # skip_requesting_account_id  = true # Skip account ID validation
  # endpoints {
  #   s3  = "http://s3.localhost.localstack.cloud:4566" # LocalStack S3 endpoint
  #   ec2 = "http://localhost:4566"
  # }
}
terraform {
  backend "s3" {
    bucket = "nour-tfstate"  # Match your bucket name
    key    = "terraform.tfstate"              # Path to state file in bucket
    region = "us-east-1"                      # Match your bucket’s region
  }
}

