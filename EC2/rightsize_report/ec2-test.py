#!/usr/bin/env python

import boto3

def scan_ec2_instances():
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.all()
    
    inst_id = []
    inst_type = []
    
    for instance in instances:
        inst_id.append(instance.id)
        inst_type.append(instance.instance_type)
    
    print("Instance IDs:", inst_id)
    print("Instance Types:", inst_type)

scan_ec2_instances()