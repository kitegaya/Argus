output "dynamodb_table_name" {
  value = aws_dynamodb_table.incidents.name
}

output "s3_bucket_name" {
  value = aws_s3_bucket.reports.bucket
}

output "sns_topic_arn" {
  value = aws_sns_topic.alerts.arn
}
