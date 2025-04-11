variable "vpc_name" {
  type        = string
  default     = "main-vpc"
  description = "provide a tag name for the vpc"
}
variable "vpc_cidr" {
  type        = string
  default     = "10.0.0.0/16"
  description = "provide a cidr for the vpc"
}
variable "vpc_reagion" {
  type        = string
  default     = "us-east"
  description = "provide a region for the vpc"
}


variable "public_subnet_count" {
  description = "Number of public subnets to create"
  type        = number
  default     = 2
}

variable "private_subnet_count" {
  description = "Number of private subnets to create"
  type        = number
  default     = 2
}

variable "availability_zones" {
  description = "AZs to distribute subnets across"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "ngw_tagname" {
  type        = string
  default     = "ngw"
  description = "provide a name for nat gateway"
}
variable "igw_tagname" {
  type        = string
  default     = "igw"
  description = "provide a name for nat gateway"
}
variable "public_rtable_tagname" {
  type        = string
  default     = "public-route-table"
  description = "provide a name for public route table"
}
variable "private_rtable_tagname" {
  type        = string
  default     = "private-route-table"
  description = "provide a name for private route table"
}