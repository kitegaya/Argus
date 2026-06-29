variable "aws_region" {
  description = "AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}

variable "unique_suffix" {
  description = "Short unique string appended to resource names for global uniqueness (e.g. your username or a random suffix)."
  type        = string
}

variable "notification_email" {
  description = "Email address to receive billing-alarm notifications via SNS. Leave empty to skip subscription."
  type        = string
  default     = ""
}
