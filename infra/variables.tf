variable "aws_region" {
  default = "us-east-1"
}

variable "unique_suffix" {
  description = "Short unique string to make resource names globally unique"
  type        = string
}

variable "notification_email" {
  description = "Email for billing alarm notifications"
  type        = string
}
