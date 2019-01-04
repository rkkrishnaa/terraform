//provider configuration
provider "aws" {
  region = "${module.global_variables.default_aws_region}"
}

//backend configuration
terraform {
  backend "consul" {
    address = "consul.stage.myorg.com"
    scheme  = "http"
    path    = "stage/terraform/rds"
  }
}

//create sns topic
resource "aws_sns_topic" "sns_topic" {
  name = "${var.sns_topic}"
}

//create subscription to sns topic
resource "aws_sns_topic_subscription" "my_subscription" {
  topic_arn = "${aws_sns_topic.sns_topic.arn}"
  protocol  = "sqs"
  endpoint  = "${var.sns_endpoint}"
  endpoint_auto_confirms = "true"
}
