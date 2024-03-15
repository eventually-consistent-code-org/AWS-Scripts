#!/usr/bin/env python

import boto3

def describe_ec2_instances():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    
    instance_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])
    
    for instance_id in instance_ids:
        print(f"This is instance: {instance_id}")
        
describe_ec2_instances()
