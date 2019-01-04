output "sns_topic_arn" {
  value = "${aws_sns_topic_subscription.my_subscription.topic_arn}"
}
