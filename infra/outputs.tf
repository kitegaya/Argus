output "dynamodb_table_name" {
  description = "DynamoDB table name — set this as DYNAMODB_TABLE in Jenkins."
  value       = aws_dynamodb_table.incidents.name
}

output "s3_bucket_name" {
  description = "S3 bucket name — set this as S3_BUCKET in Jenkins."
  value       = aws_s3_bucket.reports.bucket
}

output "sns_topic_arn" {
  description = "SNS topic ARN used for billing alerts."
  value       = aws_sns_topic.alerts.arn
}
