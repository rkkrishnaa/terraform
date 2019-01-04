import boto3
import node_definitions
from datetime import datetime
import json
import csv

# log file
time = datetime.now()
filename = 'cloudwatch'
time = str(time).split(" ")[0]+'-'+str(time).split(" ")[1].split(".")[0]+':'+str(time).split(" ")[1].split(".")[1]
cloudwatch_logfile = filename + '-' + 'alarm' + '-' + time + '.log'

# client objects
elasticache_client = boto3.client('elasticache')
cloudwatch_client = boto3.client('cloudwatch')
ec2_client = boto3.client('ec2')

# This method will create an alarm in cloudwatch.
def create_alarm(name_space=None, alarm_name=None, metric_name=None, threshold=None,
				alarm_description=None, dimension_name=None, dimension_value=None, unit=None,
				comparison_operator='GreaterThanOrEqualToThreshold', evaluation_periods=2,
				period=300, statistic='Maximum', arn=None, actions_enabled=False):

	alarm_create = cloudwatch_client.put_metric_alarm(Namespace=name_space,
													AlarmName=alarm_name,
													MetricName=metric_name,
													Threshold=threshold,
													AlarmDescription=alarm_description,
													ComparisonOperator=comparison_operator,
													EvaluationPeriods=evaluation_periods,
													Period=period,
													Statistic=statistic,
													ActionsEnabled=actions_enabled,
													AlarmActions=[arn, ],
													OKActions=[arn, ],
													InsufficientDataActions=[],
													Unit=unit,
													Dimensions=[
														{
															'Name': dimension_name,
															'Value': dimension_value
														},
													])
	print (alarm_create)
	with open(cloudwatch_logfile, 'a') as f:
		f.write('response body..' + '\n')
		f.write(json.dumps(alarm_create) + '\n')
	return alarm_create

# This method will list all the alarm names with the matched keyword
def list_alarm(alarm_prefix):
	alarm_list = []
	paginator = cloudwatch_client.get_paginator('describe_alarms')
	alarms = paginator.paginate(AlarmNamePrefix=alarm_prefix, PaginationConfig={'MaxItems': 1000, 'PageSize': 100})
	for alarm in alarms:
		for metric in alarm['MetricAlarms']:
			alarm_list.append(metric['AlarmName'])
	return alarm_list

# This method will update the selected alarm
# Update alarm is same as create_alarm method
def update_alarm():
	return 0

#This method will delete the selected alarm
def delete_alarm(alarm_list=None):
	def divide_list_into_chunk(list_name=None, chunk_max_item=2):
		for j in range(0, len(list_name), chunk_max_item):
			yield list_name[j:j + chunk_max_item]

	num_chunk = 100
	alarm_chunk = list(divide_list_into_chunk(alarm_list, num_chunk	))
	for num in range(len(alarm_chunk)):
		alarm_delete = cloudwatch_client.delete_alarms(AlarmNames=alarm_chunk[num])

# get the list of nodes in a elasticache cluster
def get_cache_node_list():
	paginator = elasticache_client.get_paginator('describe_cache_clusters')
	cachenodes = paginator.paginate(PaginationConfig={'MaxItems': 10000, 'PageSize': 100})
	cache_node_list = []
	for nodes in cachenodes:
		for i in range(len(nodes['CacheClusters'])):
			for j in range(len(node_definitions.ELASTICACHE_REDIS_CLUSTER_LIST)):
				if node_definitions.ELASTICACHE_REDIS_CLUSTER_LIST[j] in nodes['CacheClusters'][i]['CacheClusterId']:
					cache_node_list.append(nodes['CacheClusters'][i]['CacheClusterId'])
	return cache_node_list

# elasticache node
# This method will return the elasticache node type of all nodes in the list of elasticache nodes.
def get_cache_node_type():
	elasticache_node_list = get_cache_node_list()
	cluster_metadata = {}

	for i in range(len(elasticache_node_list)):
		cluster_info = elasticache_client.describe_cache_clusters(CacheClusterId=elasticache_node_list[i],
																ShowCacheNodeInfo=False,
																ShowCacheClustersNotInReplicationGroups=False
																)
		for info in cluster_info['CacheClusters']:
			cluster_metadata[info['CacheClusterId']] = { }
			cluster_metadata[info['CacheClusterId']]['CacheClusterId'] = info['CacheClusterId']
			cluster_metadata[info['CacheClusterId']]['CacheNodeType'] = info['CacheNodeType']
	return cluster_metadata

# This method will create a cloudwatch alarm for the selected elasticache cluster nodes
def create_alarm_elasticache(alert_level):
	elasticache_node_list = get_cache_node_list()
	alert_level = alert_level
	if alert_level == 'Warning':
		node_definitions.elasticache_actions_enabled = False
	cache_node_type = get_cache_node_type()
	for i in range(len(elasticache_node_list)):
		cluster = elasticache_node_list[i]
		for metric, unit in node_definitions.ELASTICACHE_METRICS_DICT.iteritems():
			Metric = metric
			node_definitions.elasticache_comparison_operator = 'GreaterThanOrEqualToThreshold'
			alarmDescription = 'Cloudwatch alarm for cluster' + cluster + '-' + metric + '-' + alert_level + ' alert'
			AlarmName = 'AWS-Elasticache-' + cluster + '-' + metric + '-' + alert_level
			node_type = cache_node_type[cluster]['CacheNodeType']
			if Metric == 'EngineCPUUtilization' or Metric == 'CPUUtilization':
				MetricName = 'vCPU'
			elif Metric == 'NetworkBytesIn' or Metric == 'NetworkBytesOut':
				MetricName = 'Network'
			elif Metric == 'FreeableMemory':
				MetricName = 'Memory'
				node_definitions.elasticache_comparison_operator = 'LessThanOrEqualToThreshold'
			elif Metric == 'CurrConnections':
				MetricName = 'CurrConnections'
			else:
				print('No metrics')

			if Metric == 'NetworkBytesIn':
				node_metric_value = node_definitions.ELASTICACHE_NODE_TYPE[node_type][MetricName]
				if alert_level == 'Warning':
					Threshold = (node_definitions.ELASTICACHE_ALARM_THRESHOLDS['NetworkBytesIn_Warning']/100.0) * node_metric_value
				else:
					Threshold = (node_definitions.ELASTICACHE_ALARM_THRESHOLDS['NetworkBytesIn_Critical']/100.0) * node_metric_value
			elif Metric == 'NetworkBytesOut':
				node_metric_value = node_definitions.ELASTICACHE_NODE_TYPE[node_type][MetricName]
				if alert_level == 'Warning':
					Threshold = (node_definitions.ELASTICACHE_ALARM_THRESHOLDS['NetworkBytesOut_Warning'] / 100.0) * node_metric_value
				else:
					Threshold = (node_definitions.ELASTICACHE_ALARM_THRESHOLDS['NetworkBytesOut_Critical'] / 100.0) * node_metric_value

			elif Metric == 'EngineCPUUtilization':
				node_metric_value = node_definitions.ELASTICACHE_NODE_TYPE[node_type][MetricName]
				if alert_level == 'Warning':
					Threshold = node_definitions.ELASTICACHE_ALARM_THRESHOLDS['EngineCPUUtilization_Warning']
					print(Threshold)
					#Threshold = (node_definitions.ELASTICACHE_ALARM_THRESHOLDS['EngineCPUUtilization_Warning']/100) * (100/node_metric_value)
				else:
					Threshold = node_definitions.ELASTICACHE_ALARM_THRESHOLDS['EngineCPUUtilization_Critical']
					print(Threshold)
					#Threshold = (node_definitions.ELASTICACHE_ALARM_THRESHOLDS['EngineCPUUtilization_Critical']/100) * (100/node_metric_value)

			elif Metric == 'CPUUtilization':
				node_metric_value = node_definitions.ELASTICACHE_NODE_TYPE[node_type][MetricName]
				if alert_level == 'Warning':
					Threshold = node_definitions.ELASTICACHE_ALARM_THRESHOLDS['CPUUtilization_Warning']
					print(Threshold)
					#Threshold = (node_definitions.ELASTICACHE_ALARM_THRESHOLDS['CPUUtilization_Warning']/100.0) * (100/node_metric_value)
				else:
					Threshold = node_definitions.ELASTICACHE_ALARM_THRESHOLDS['CPUUtilization_Critical']
					print(Threshold)
					#Threshold = (node_definitions.ELASTICACHE_ALARM_THRESHOLDS['CPUUtilization_Critical']/100.0) * (100/node_metric_value)

			elif Metric == 'FreeableMemory':
				node_metric_value = node_definitions.ELASTICACHE_NODE_TYPE[node_type][MetricName]
				if alert_level == 'Warning':
					Threshold = (node_definitions.ELASTICACHE_ALARM_THRESHOLDS['FreeableMemory_Warning']/100.0) * node_metric_value
				else:
					Threshold = (node_definitions.ELASTICACHE_ALARM_THRESHOLDS['FreeableMemory_Critical']/100.0) * node_metric_value

			elif MetricName == 'CurrConnections':
				node_metric_value = node_definitions.ELASTICACHE_NODE_TYPE[node_type][MetricName]
				if alert_level == 'Warning':
					Threshold = (node_definitions.ELASTICACHE_ALARM_THRESHOLDS['CurrConnections_Warning'] / 100.0) * node_metric_value
				else:
					Threshold = (node_definitions.ELASTICACHE_ALARM_THRESHOLDS['CurrConnections_Critical'] / 100.0) * node_metric_value
			else:
				print('Elasticache')

			request_body = {}
			request_body['name_space'] = node_definitions.elasticache_namespace
			request_body['alarm_name'] = AlarmName
			request_body['metric_name'] = Metric
			request_body['threshold'] = Threshold
			request_body['alarm_description'] = alarmDescription
			request_body['dimension_name'] = node_definitions.elasticache_dimension_name
			request_body['dimension_value'] = cluster
			request_body['unit'] = unit
			request_body['comparison_operator'] = node_definitions.elasticache_comparison_operator
			request_body['period'] = node_definitions.elasticache_period
			request_body['statistic'] = node_definitions.elasticache_statistic
			request_body['actions_enabled'] = str(node_definitions.elasticache_actions_enabled)
			request_body['sns_arn'] = node_definitions.sns_arn
			print(request_body)

			with open(cloudwatch_logfile, 'a') as f:
				f.write('creating alarm with request body..' + '\n')
				f.write(json.dumps(request_body) + '\n')

			create_alarm(name_space=node_definitions.elasticache_namespace,
						alarm_name=AlarmName,
						metric_name=Metric,
						threshold=Threshold,
						alarm_description=alarmDescription,
						dimension_name=node_definitions.elasticache_dimension_name,
						dimension_value=cluster,
						unit=unit,
						comparison_operator=node_definitions.elasticache_comparison_operator,
                        evaluation_periods=node_definitions.elasticache_evaluation_periods,
						period=node_definitions.elasticache_period,
						statistic=node_definitions.elasticache_statistic,
						arn=node_definitions.sns_arn,
						actions_enabled=node_definitions.elasticache_actions_enabled)

# ec2 instance
# This method will return the instance id and instance type for all the sand prod running instances
def get_ec2_instance_type():
	instance_count = 0
	running_instances = 0
	stopped_instances = 0
	unknown_instances = 0
	ec2instance_metadata = {}
	paginator = ec2_client.get_paginator('describe_instances')
	instance_list = paginator.paginate(Filters=[{'Name':'tag:service','Values':['devops']},{'Name':'tag:env','Values':['prod']}],PaginationConfig={'MaxItems': 10000, 'PageSize': 10000})

	for page in instance_list:
		for instances in page['Reservations']:
			for instance in instances['Instances']:
				instance_count = instance_count + 1
				if instance['State']['Code'] == 16:
					running_instances = running_instances + 1
					instance_state = 'Running'
					ec2instance_metadata[instance['InstanceId']] = {}
					ec2instance_metadata[instance['InstanceId']]['InstanceId'] = instance['InstanceId']
					ec2instance_metadata[instance['InstanceId']]['InstanceType'] = instance['InstanceType']
					ec2instance_metadata[instance['InstanceId']]['PrivateIpAddress'] = instance['PrivateIpAddress']
					ec2instance_metadata[instance['InstanceId']]['InstanceState'] = instance_state
				elif instance['State']['Code'] == 80:
					stopped_instances = stopped_instances + 1
					instance_state = 'Stopped'
				else:
					unknown_instances = unknown_instances + 1
					instance_state = 'Unknown'

	print('instance count with the specified tag: ', instance_count)
	print('running state instances with the specified tag: ', running_instances)
	print('stopped state instances with the specified tag: ', stopped_instances)
	print('unknown state instances with the specified tag: ', unknown_instances)

	return ec2instance_metadata

# This method will create an alarm in cloudwatch for the selected ec2 instances
def create_alarm_ec2(alert_level):
	# cloudwatch alarm properties
	nameSpace = 'AWS/EC2'
	statistic = 'Maximum'
	period = 300
	comparison_operator = 'GreaterThanOrEqualToThreshold'
	evaluation_periods = 1
	actions_enabled = True
	dimension_name = 'InstanceId'

	alert_level = alert_level
	actions_enabled = True
	if alert_level == 'Warning':
		actions_enabled = False

	ec2_instance_type = get_ec2_instance_type()
	for instance_id in ec2_instance_type:
		instance = instance_id
		for metric, unit in node_definitions.EC2_METRICS_DICT.iteritems():
			Metric = metric
			comparison_operator = 'GreaterThanOrEqualToThreshold'
			alarmDescription = 'Cloudwatch alarm for ec2 instance' + instance + '-' + metric + '-' + alert_level + ' alert'
			AlarmName = 'AWS-EC2-' + instance + '-' + metric + '-' + alert_level
			node_type = ec2_instance_type[instance]['InstanceType']
			if Metric == 'CPUUtilization':
				MetricName = 'vCPU'
			elif Metric == 'NetworkIn' or Metric == 'NetworkOut':
				MetricName = 'Network'
			else:
				print('No metrics')

			if Metric == 'NetworkIn':
				node_metric_value = node_definitions.EC2_NODE_TYPE[node_type][MetricName]
				if alert_level == 'Warning':
					Threshold = (node_definitions.EC2_ALARM_THRESHOLDS['NetworkIn_Warning']/100.0) * node_metric_value
				else:
					Threshold = (node_definitions.EC2_ALARM_THRESHOLDS['NetworkIn_Critical']/100.0) * node_metric_value
			elif Metric == 'NetworkOut':
				node_metric_value = node_definitions.EC2_NODE_TYPE[node_type][MetricName]
				if alert_level == 'Warning':
					Threshold = (node_definitions.EC2_ALARM_THRESHOLDS['NetworkOut_Warning'] / 100.0) * node_metric_value
				else:
					Threshold = (node_definitions.EC2_ALARM_THRESHOLDS['NetworkOut_Critical'] / 100.0) * node_metric_value
			elif Metric == 'CPUUtilization':
				node_metric_value = node_definitions.EC2_NODE_TYPE[node_type][MetricName]
				if alert_level == 'Warning':
					Threshold = node_definitions.EC2_ALARM_THRESHOLDS['CPUUtilization_Warning']
				else:
					Threshold = node_definitions.EC2_ALARM_THRESHOLDS['CPUUtilization_Critical']
			else:
				print('EC2')

			request_body = {}
			request_body['name_space'] = nameSpace
			request_body['alarm_name'] = AlarmName
			request_body['metric_name'] = Metric
			request_body['threshold'] = Threshold
			request_body['alarm_description'] = alarmDescription
			request_body['dimension_name'] = dimension_name
			request_body['dimension_value'] = instance
			request_body['unit'] = unit
			request_body['comparison_operator'] = comparison_operator
			request_body['period'] = period
			request_body['statistic'] = statistic
			request_body['actions_enabled'] = str(actions_enabled)
			request_body['sns_arn'] = node_definitions.sns_arn
			print (request_body)
			print ('creating alarm..')

			create_alarm(name_space=nameSpace,
						alarm_name=AlarmName,
						metric_name=Metric,
						threshold=Threshold,
						alarm_description=alarmDescription,
						dimension_name=dimension_name,
						dimension_value=instance,
						unit=unit,
						comparison_operator=comparison_operator,
						period=period,
						statistic=statistic,
						actions_enabled=actions_enabled)



def generate_csv_report():
	csv_file = 'cloudwatch-alarm-' + time + '.csv'
	fieldnames = ['AlarmName', 'Statistic',
				  'MetricName', 'Namespace',
				  'StateValue', 'ActionsEnabled',
				  'AlarmActions', 'StateReason',
				  'Threshold', 'Unit',
				  'Period',
				  'EvaluationPeriods', 'ComparisonOperator',
				  'DimensionName', 'DimensionValue']
	with open(csv_file, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()

	alarm_lists = list_alarm(alarm_prefix='AWS-Elasticache')

	def divide_list_into_chunks(list_name=None, chunk_max_item=2):
		for j in range(0, len(list_name), chunk_max_item):
			yield list_name[j:j + chunk_max_item]

	num_chunk = 2
	alarm_chunk = list(divide_list_into_chunks(alarm_lists, num_chunk))
	#print(len(alarm_chunk))
	for num in range(len(alarm_chunk)):
		#print(len(alarm_chunk[num]))
		resp = cloudwatch_client.describe_alarms(AlarmNames=alarm_chunk[num])
		for j in range(len(resp)):
			try:
				with open(csv_file, 'a') as csvfile:
					writer = csv.writer(csvfile, delimiter=',')
					writer.writerow([resp['MetricAlarms'][j]['AlarmName'], resp['MetricAlarms'][j]['Statistic'],
									resp['MetricAlarms'][j]['MetricName'], resp['MetricAlarms'][j]['Namespace'],
									resp['MetricAlarms'][j]['StateValue'], resp['MetricAlarms'][j]['ActionsEnabled'],
									resp['MetricAlarms'][j]['AlarmActions'], resp['MetricAlarms'][j]['StateReason'],
									resp['MetricAlarms'][j]['Threshold'], resp['MetricAlarms'][j]['Unit'],
									resp['MetricAlarms'][j]['Period'],
									resp['MetricAlarms'][j]['EvaluationPeriods'], resp['MetricAlarms'][j]['ComparisonOperator'],
									resp['MetricAlarms'][j]['Dimensions'][0]['Name'], resp['MetricAlarms'][j]['Dimensions'][0]['Value']
					])
			except KeyError:
				pass
	count = 0
	print ('alarm list:')
	for i in range(len(alarm_lists)):
		count = count + 1
		print (count,'. ' + alarm_lists[i])



if __name__ == '__main__':
	# elascticache
	create_alarm_elasticache(alert_level='Warning')
	create_alarm_elasticache(alert_level='Critical')

	#ec2
	create_alarm_ec2(alert_level='Warning')
	create_alarm_ec2(alert_level='Critical')

	#reports
	generate_csv_report()