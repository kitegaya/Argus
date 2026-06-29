provider "aws" {
  region = var.aws_region
}

# ── DynamoDB ───────────────────────────────────────────────────────────────────
resource "aws_dynamodb_table" "incidents" {
  name         = "argus-incidents-${var.unique_suffix}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "incident_id"

  attribute {
    name = "incident_id"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Name        = "argus-incidents"
    Environment = "argus-project"
  }
}

# ── S3 ─────────────────────────────────────────────────────────────────────────
resource "aws_s3_bucket" "reports" {
  bucket = "argus-reports-${var.unique_suffix}"

  tags = {
    Name        = "argus-reports"
    Environment = "argus-project"
  }
}

resource "aws_s3_bucket_versioning" "reports" {
  bucket = aws_s3_bucket.reports.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "reports" {
  bucket                  = aws_s3_bucket.reports.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ── SNS ────────────────────────────────────────────────────────────────────────
resource "aws_sns_topic" "alerts" {
  name = "argus-alerts-${var.unique_suffix}"

  tags = {
    Name        = "argus-alerts"
    Environment = "argus-project"
  }
}

resource "aws_sns_topic_subscription" "billing_email" {
  count     = var.notification_email != "" ? 1 : 0
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.notification_email
}

# ── CloudWatch Billing Guardrail ───────────────────────────────────────────────
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
  alarm_description   = "Fires when estimated AWS charges exceed $1 in a 6-hour window."

  dimensions = {
    Currency = "USD"
  }

  tags = {
    Name        = "argus-billing-guardrail"
    Environment = "argus-project"
  }
}
