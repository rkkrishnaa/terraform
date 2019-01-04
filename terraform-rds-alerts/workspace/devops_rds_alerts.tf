module "u1-db" {
  source = "../modules/rds_alerts"
  dbinstanceId = "u1-db"
  aws_sns_topic_subscription = "${aws_sns_topic.sns_topic.arn}"
  period = "${module.global_variables.period}"
  statistic = "${module.global_variables.statistic}"
  actions_enabled = "${module.global_variables.actions_enabled}"
  evaluation_periods = "${module.global_variables.evaluation_periods}"
  pod = "${module.global_variables.pod}"
  namespace = "${module.global_variables.namespace}"
  cpu_threshold_warning = "${module.global_variables.rds_cpu_threshold_warning}"
  cpu_threshold_critical = "${module.global_variables.rds_cpu_threshold_critical}"
  freememory_threshold_warning = "${module.global_variables.rds_freememory_threshold_warning}"
  freememory_threshold_critical = "${module.global_variables.rds_freememory_threshold_critical}"
  diskspace_threshold_warning = "${module.global_variables.rds_diskspace_threshold_warning}"
  diskspace_threshold_critical = "${module.global_variables.rds_diskspace_threshold_critical}"
  rds_connections_threshold_warning = "${module.global_variables.rds_connections_threshold_critical}"
  rds_connections_threshold_critical = "${module.global_variables.rds_connections_threshold_critical}"
  rds_read_latency_threshold = "${module.global_variables.rds_read_latency_threshold}"
  rds_write_latency_threshold = "${module.global_variables.rds_write_latency_threshold}"
  rds_replica_lag_threshold = "${module.global_variables.rds_replica_lag_threshold}"
}