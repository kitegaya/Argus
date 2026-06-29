provider "aws" {
  region = var.aws_region
}

resource "aws_dynamodb_table" "incidents" {
  name           = "argus-incidents-${var.unique_suffix}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "incident_id"

  attribute {
    name = "incident_id"
    type = "S"
  }

  tags = {
    Name        = "argus-incidents"
    Environment = "argus-project"
  }
}

resource "aws_s3_bucket" "reports" {
  bucket = "argus-reports-${var.unique_suffix}"

  tags = {
    Name        = "argus-reports"
    Environment = "argus-project"
  }
}

resource "aws_sns_topic" "alerts" {
  name = "argus-alerts-${var.unique_suffix}"

  tags = {
    Name        = "argus-alerts"
    Environment = "argus-project"
  }
}

resource "aws_cloudwatch_metric_alarm" "billing_guardrail" {
  alarm_name          = "argus-billing-guardrail-${var.unique_suffix}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "EstimatedCharges"
  namespace           = "AWS/Billing"
  period              = 21600
  statistic           = "Maximum"
  threshold           = 1
  alarm_actions       = [aws_sns_topic.alerts.arn]

  dimensions = {
    Currency = "USD"
  }

  tags = {
    Name        = "argus-billing-guardrail"
    Environment = "argus-project"
  }
}
