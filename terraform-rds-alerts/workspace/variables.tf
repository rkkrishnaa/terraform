module "global_variables" {
  source="../global_variables/"
}

variable "sns_topic" {
  default = "devops-alerts"
}

variable "sns_endpoint" {
  default = "arn:aws:sqs:ap-southeast-1:aws-acct-no:alerts"
}
