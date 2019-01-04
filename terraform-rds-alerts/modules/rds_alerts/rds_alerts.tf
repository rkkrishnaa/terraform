# cpu alerts
resource "aws_cloudwatch_metric_alarm" "rds-cpu-alerts-warning" {
  alarm_name          = "AWS-RDS-${var.pod}-${var.dbinstanceId}-db-cpu-warning"
  metric_name         = "CPUUtilization"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  alarm_description   = "This metric monitors rds cpu utilization for ${var.dbinstanceId}"
  namespace           = "${var.namespace}"
  threshold           = "${var.cpu_threshold_warning}"
  evaluation_periods  = "${var.evaluation_periods}"
  period              = "${var.period}"
  statistic           = "${var.statistic}"
  actions_enabled     = "${var.actions_enabled}"

  dimensions {
    DBInstanceIdentifier = "${var.dbinstanceId}"
  }

  alarm_actions = ["${var.aws_sns_topic_subscription}"]
  ok_actions    = ["${var.aws_sns_topic_subscription}"]
}

resource "aws_cloudwatch_metric_alarm" "rds-cpu-alerts-critical" {
  alarm_name          = "AWS-RDS-${var.pod}-${var.dbinstanceId}-db-cpu-critical"
  metric_name         = "CPUUtilization"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  alarm_description   = "This metric monitors rds cpu utilization for ${var.dbinstanceId}"
  namespace           = "${var.namespace}"
  threshold           = "${var.cpu_threshold_critical}"
  evaluation_periods  = "${var.evaluation_periods}"
  period              = "${var.period}"
  statistic           = "${var.statistic}"
  actions_enabled     = "${var.actions_enabled}"

  dimensions {
    DBInstanceIdentifier = "${var.dbinstanceId}"
  }

  alarm_actions = ["${var.aws_sns_topic_subscription}"]
  ok_actions    = ["${var.aws_sns_topic_subscription}"]
}

# memory alerts
resource "aws_cloudwatch_metric_alarm" "rds-free-memory-warning" {
  alarm_name          = "AWS-RDS-${var.pod}-${var.dbinstanceId}-rds-free-memory-warning"
  metric_name         = "FreeableMemory"
  comparison_operator = "LessThanThreshold"
  alarm_description   = "This metric monitors rds free memory for ${var.dbinstanceId}"
  namespace           = "${var.namespace}"
  threshold           = "${var.freememory_threshold_warning}"
  evaluation_periods  = "${var.evaluation_periods}"
  period              = "${var.period}"
  statistic           = "${var.statistic}"
  actions_enabled     = "${var.actions_enabled}"

  dimensions {
    DBInstanceIdentifier = "${var.dbinstanceId}"
  }

  alarm_actions = ["${var.aws_sns_topic_subscription}"]
  ok_actions    = ["${var.aws_sns_topic_subscription}"]
}

resource "aws_cloudwatch_metric_alarm" "rds-free-memory-critical" {
  alarm_name          = "AWS-RDS-${var.pod}-${var.dbinstanceId}-rds-free-memory-critical"
  metric_name         = "FreeableMemory"
  comparison_operator = "LessThanThreshold"
  alarm_description   = "This metric monitors rds free memory for ${var.dbinstanceId}"
  namespace           = "${var.namespace}"
  threshold           = "${var.freememory_threshold_critical}"
  evaluation_periods  = "${var.evaluation_periods}"
  period              = "${var.period}"
  statistic           = "${var.statistic}"
  actions_enabled     = "${var.actions_enabled}"

  dimensions {
    DBInstanceIdentifier = "${var.dbinstanceId}"
  }

  alarm_actions = ["${var.aws_sns_topic_subscription}"]
  ok_actions    = ["${var.aws_sns_topic_subscription}"]
}

# disk space alerts
resource "aws_cloudwatch_metric_alarm" "rds-disk-space-warning" {
  alarm_name          = "AWS-RDS-${var.pod}-${var.dbinstanceId}-rds-disk-space-warning"
  metric_name         = "FreeStorageSpace"
  comparison_operator = "LessThanThreshold"
  alarm_description   = "This metric monitors rds free disk space for ${var.dbinstanceId}"
  namespace           = "${var.namespace}"
  threshold           = "${var.diskspace_threshold_warning}"
  evaluation_periods  = "${var.evaluation_periods}"
  period              = "${var.period}"
  statistic           = "${var.statistic}"
  actions_enabled     = "${var.actions_enabled}"

  dimensions {
    DBInstanceIdentifier = "${var.dbinstanceId}"
  }

  alarm_actions = ["${var.aws_sns_topic_subscription}"]
  ok_actions    = ["${var.aws_sns_topic_subscription}"]
}

resource "aws_cloudwatch_metric_alarm" "rds-disk-space-critical" {
  alarm_name          = "AWS-RDS-${var.pod}-${var.dbinstanceId}-rds-disk-space-critical"
  metric_name         = "FreeStorageSpace"
  comparison_operator = "LessThanThreshold"
  alarm_description   = "This metric monitors rds free disk space for ${var.dbinstanceId}"
  namespace           = "${var.namespace}"
  threshold           = "${var.diskspace_threshold_critical}"
  evaluation_periods  = "${var.evaluation_periods}"
  period              = "${var.period}"
  statistic           = "${var.statistic}"
  actions_enabled     = "${var.actions_enabled}"

  dimensions {
    DBInstanceIdentifier = "${var.dbinstanceId}"
  }

  alarm_actions = ["${var.aws_sns_topic_subscription}"]
  ok_actions    = ["${var.aws_sns_topic_subscription}"]
}

# database connections
resource "aws_cloudwatch_metric_alarm" "rds-connections-warning" {
  alarm_name          = "AWS-RDS-${var.pod}-${var.dbinstanceId}-rds-connections-warning"
  metric_name         = "DatabaseConnections"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  alarm_description   = "RDS Maximum connection Alarm for ${var.dbinstanceId}"
  namespace           = "${var.namespace}"
  threshold           = "${var.rds_connections_threshold_warning}"
  evaluation_periods  = "${var.evaluation_periods}"
  period              = "${var.period}"
  statistic           = "${var.statistic}"
  actions_enabled     = "${var.actions_enabled}"

  dimensions {
    DBInstanceIdentifier = "${var.dbinstanceId}"
  }

  alarm_actions = ["${var.aws_sns_topic_subscription}"]
  ok_actions    = ["${var.aws_sns_topic_subscription}"]
}

resource "aws_cloudwatch_metric_alarm" "rds-connections-critical" {
  alarm_name          = "AWS-RDS-${var.pod}-${var.dbinstanceId}-rds-connections-critical"
  metric_name         = "DatabaseConnections"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  alarm_description   = "RDS Maximum connection Alarm for ${var.dbinstanceId}"
  namespace           = "${var.namespace}"
  threshold           = "${var.rds_connections_threshold_critical}"
  evaluation_periods  = "${var.evaluation_periods}"
  period              = "${var.period}"
  statistic           = "${var.statistic}"
  actions_enabled     = "${var.actions_enabled}"

  dimensions {
    DBInstanceIdentifier = "${var.dbinstanceId}"
  }

  alarm_actions = ["${var.aws_sns_topic_subscription}"]
  ok_actions    = ["${var.aws_sns_topic_subscription}"]
}

# read latency
resource "aws_cloudwatch_metric_alarm" "rds-read-latency" {
  alarm_name          = "AWS-RDS-${var.pod}-${var.dbinstanceId}-read-latency"
  metric_name         = "ReadLatency"
  comparison_operator = "GreaterThanThreshold"
  alarm_description   = "read latency for ${var.dbinstanceId}"
  namespace           = "${var.namespace}"
  threshold           = "${var.rds_read_latency_threshold}"
  statistic           = "${var.statistic}"
  evaluation_periods  = "${var.evaluation_periods}"
  period              = "${var.period}"
  actions_enabled     = "${var.actions_enabled}"

  dimensions {
    DBInstanceIdentifier = "${var.dbinstanceId}"
  }

  alarm_actions = ["${var.aws_sns_topic_subscription}"]
  ok_actions    = ["${var.aws_sns_topic_subscription}"]
}

# write latency
resource "aws_cloudwatch_metric_alarm" "rds-write-latency" {
  alarm_name          = "AWS-RDS-${var.pod}-${var.dbinstanceId}-rds-write-latency"
  metric_name         = "WriteLatency"
  comparison_operator = "GreaterThanThreshold"
  alarm_description   = "write latency for ${var.dbinstanceId}"
  namespace           = "${var.namespace}"
  threshold           = "${var.rds_write_latency_threshold}"
  statistic           = "${var.statistic}"
  evaluation_periods  = "${var.evaluation_periods}"
  period              = "${var.period}"
  actions_enabled     = "${var.actions_enabled}"

  dimensions {
    DBInstanceIdentifier = "${var.dbinstanceId}"
  }

  alarm_actions = ["${var.aws_sns_topic_subscription}"]
  ok_actions    = ["${var.aws_sns_topic_subscription}"]
}

# replica lag
resource "aws_cloudwatch_metric_alarm" "rds_replica_lag" {
  alarm_name          = "AWS-RDS-${var.pod}-${var.dbinstanceId} alarm-rds-reader-ReplicaLag"
  metric_name         = "ReplicaLag"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  alarm_description   = "RDS replica lag alarm for ${var.dbinstanceId}"
  namespace           = "${var.namespace}"
  threshold           = "${var.rds_replica_lag_threshold}"
  evaluation_periods  = "${var.evaluation_periods}"
  period              = "${var.period}"
  statistic           = "${var.statistic}"
  actions_enabled     = "${var.actions_enabled}"

  dimensions {
    DBInstanceIdentifier = "${var.dbinstanceId}"
  }

  alarm_actions = ["${var.aws_sns_topic_subscription}"]
  ok_actions    = ["${var.aws_sns_topic_subscription}"]
}