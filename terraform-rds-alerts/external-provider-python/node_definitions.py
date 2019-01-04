# static values

# sns arn to get email notification about the event
sns_arn = 'arn:aws:sns:ap-southeast-1:aws_acct_number:cw_alerts'

# Elasticache
# This list contains the name of sand redis elasticache cluster
ELASTICACHE_REDIS_CLUSTER_LIST = [
	'cluster-1',
	'cluster-2',
	'cluster-3'
]

#This dict contains an information about vCPU, Memory in Gigabits, Network in Gigabytes, CurrConnections based on cache node type.
#Update dictionary if new node is added whose type is not mentioned here.
#vCPU -
#Memory -
#Network -
#CurrConnections -

ELASTICACHE_NODE_TYPE = {
    'cache.t2.micro': {
        'vCPU': 1,
		'Memory': 0.555 * 1000000000,
		'Network': 0.25 * 1250000000,
		'CurrConnections': 500
    },
    'cache.t2.small': {
        'vCPU': 1,
		'Memory': 1.55 * 1000000000,
		'Network': 0.25 * 1250000000,
		'CurrConnections': 1000
    },
    'cache.t2.medium': {
		'vCPU': 2,
		'Memory': 3.22 * 1000000000,
		'Network': 0.25 * 1250000000,
		'CurrConnections': 1500
	},
	'cache.r4.large': {
		'vCPU': 2,
		'Memory': 12.03 * 1000000000,
		'Network': 10 * 1250000000,
		'CurrConnections': 4000
	},
	'cache.r4.xlarge': {
		'vCPU': 4,
		'Memory': 25.05 * 1000000000,
		'Network': 10 * 1250000000,
		'CurrConnections': 8000
	},
	'cache.r4.2xlarge': {
		'vCPU': 8,
		'Memory_in_GiB': 50.47,
		'Memory': 50.47 * 1000000000,
		'Network': 10 * 1250000000,
		'CurrConnections': 9000
	},
	'cache.r4.4xlarge': {
		'vCPU': 16,
		'Memory': 101.38 * 1000000000,
		'Network': 10 * 1250000000,
		'CurrConnections': 12000
	},
	'cache.r3.large': {
		'vCPU': 2,
		'Memory': 13.5 * 1000000000,
		'Network': 0.50 * 1250000000,
		'CurrConnections': 4000
	},
	'cache.r3.xlarge': {
		'vCPU': 4,
		'Memory': 28.4 * 1000000000,
		'Network': 0.69 * 1250000000,
		'CurrConnections': 8000
	},
	'cache.m4.large': {
		'vCPU': 2,
		'Memory': 6.42 * 1000000000,
		'Network': 0.45 * 1250000000,
		'CurrConnections': 8000
	}
}

# This dict contains an information about elasticache metric dimension and its unit.
# Update dictionary if any new metric dimension has to monitored and whose dimension is not mentioned here.
ELASTICACHE_METRICS_DICT = {
	'CPUUtilization': 'Percent',
	'FreeableMemory': 'Bytes',
	'NetworkBytesIn': 'Bytes',
	'NetworkBytesOut': 'Bytes',
	'CurrConnections': 'Count',
	'EngineCPUUtilization': 'Percent'
}

#EC2
#This dict contains an information about vCPU, Memory in Gigabits, Network in Gigabytes, CurrConnections based on cache node type.
#Update dictionary if new node is added whose type is not mentioned here.
EC2_NODE_TYPE = {
	'c4.4xlarge': {
		'vCPU': 16,
		'Memory': 30 * 1250000000,
		'Network': 10 * 1250000000
	},
	'c4.2xlarge': {
		'vCPU': 8,
		'Memory': 15 * 1250000000,
		'Network': 0.45 * 1250000000
	},
	'c4.xlarge': {
		'vCPU': 4,
		'Memory': 7.5 * 1250000000,
		'Network': 0.45 * 1250000000
	},
	'c4.large': {
		'vCPU': 2,
		'Memory': 3.75 * 1250000000,
		'Network': 0.45 * 1250000000
	},
	'm4.2xlarge': {
		'vCPU': 8,
		'Memory': 32 * 1250000000,
		'Network': 0.45 * 1250000000
	},
	'm4.xlarge': {
		'vCPU': 4,
		'Memory': 16 * 1250000000,
		'Network': 0.45 * 1250000000
	},
	'm4.large': {
		'vCPU': 2,
		'Memory': 8 * 1250000000,
		'Network': 0.45 * 1250000000
	},
	't2.large': {
		'vCPU': 2,
		'Memory': 8 * 1250000000,
		'Network': 0.45 * 1250000000
	},
	't2.medium': {
		'vCPU': 2,
		'Memory': 4 * 1250000000,
		'Network': 0.45 * 1250000000
	},
	't2.small': {
		'vCPU': 1,
		'Memory': 2 * 1250000000,
		'Network': 0.45 * 1250000000
	}
}

# This dict contains an information about ec2 metric dimension and its unit.
# Update dictionary if any new metric dimension has to monitored and whose dimension is not mentioned here.

EC2_METRICS_DICT = {
	'CPUUtilization': 'Percent',
	'NetworkIn': 'Bytes',
	'NetworkOut': 'Bytes'
}

# This dict contains warning and critical thresholds for all elasticache nodes in a cluster.
ELASTICACHE_ALARM_THRESHOLDS = {
	'CPUUtilization_Warning': 85.0,
	'CPUUtilization_Critical': 90.0,
	'FreeableMemory_Warning': 20.0,
	'FreeableMemory_Critical': 10.0,
	'NetworkBytesIn_Warning': 30.0,
	'NetworkBytesIn_Critical': 40.0,
	'NetworkBytesOut_Warning': 30.0,
	'NetworkBytesOut_Critical': 40.0,
	'CurrConnections_Warning': 80.0,
	'CurrConnections_Critical': 90.0,
	'EngineCPUUtilization_Warning': 50.0,
	'EngineCPUUtilization_Critical': 60.0
}

# This dict contains warning and critical thresholds for all sand prod ec2 instances.
EC2_ALARM_THRESHOLDS = {
	'CPUUtilization_Warning': 65.0,
	'CPUUtilization_Critical': 75.0,
	'NetworkIn_Warning': 65.0,
	'NetworkIn_Critical': 75.0,
	'NetworkOut_Warning': 65.0,
	'NetworkOut_Critical': 75.0
}

# alarm properties
elasticache_namespace = 'AWS/ElastiCache'
elasticache_statistic = 'Maximum'
elasticache_period = 300
elasticache_comparison_operator = 'GreaterThanOrEqualToThreshold'
elasticache_evaluation_periods = 2
elasticache_actions_enabled = True
elasticache_dimension_name = 'CacheClusterId'