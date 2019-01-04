//general
output "evaluation_periods" {
  description = ""
  value = "2"
}

output "period" {
  description = ""
  value = "120"
}

output "statistic" {
  description = ""
  value = "Average"
}

output "actions_enabled" {
  description = ""
  value = "true"
}

output "aws_sns_topic_arn" {
  description = ""
  value = "devops-alerts"
}

// rds
output "namespace" {
  description = ""
  value = "AWS/RDS"
}

output "rds_cpu_threshold_warning" {
  description = ""
  value = "50.0"
}

output "rds_cpu_threshold_critical" {
  description = ""
  value = "60.0"
}

output "rds_freememory_threshold_warning" {
  description = ""
  value = "1024.0"
}

output "rds_freememory_threshold_critical" {
  description = ""
  value = "512.0"
}

output "rds_diskspace_threshold_warning" {
  description = ""
  value = "4096"
}

output "rds_diskspace_threshold_critical" {
  description = ""
  value = "2048"
}

output "rds_connections_threshold_warning" {
  description = ""
  value = ""
}

output "rds_connections_threshold_critical" {
  description = ""
  value = "200"
}

output "rds_read_latency_threshold" {
  description = ""
  value = "1"
}

output "rds_write_latency_threshold" {
  description = ""
  value = "1"
}

output "rds_replica_lag_threshold" {
  description = ""
  value = "1"
}

// redis elasticache cluster
output "redis_engine_cpu_utilization_threshold_warning" {
  value = "50.0"
}

output "redis_engine_cpu_utilization_threshold_critical" {
  value = "60.0"
}

output "redis_cpu_utilization_threshold_warning" {
  value = "50.0"
}

output "redis_cpu_utilization_threshold_critical" {
  value = "60.0"
}

output "redis_freeable_memory_threshold_warning" {
  value = "2048"
}

output "redis_freeable_memory_threshold_critical" {
  value = "1024"
}

output "redis_network_bytes_in_threshold_warning" {
  value = "1024"
}

output "redis_network_bytes_in_threshold_critical" {
  value = "2048"
}

output "redis_network_bytes_out_threshold_warning" {
  value = "1024"
}

output "redis_network_bytes_out_threshold_critical" {
  value = "2048"
}

output "redis_curr_connections_threshold_warning" {
  value = "100"
}

output "redis_curr_connections_threshold_critical" {
  value = "200"
}
