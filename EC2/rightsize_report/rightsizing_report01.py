#!/usr/bin/env python

import boto3
import csv
import sys
import logging

# Setup logging config
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("rightsizing_log.txt"),
        logging.StreamHandler(sys.stdout)
    ]
)
logging.info("importing ec2 data from aws... \r")

def describe_ec2_instances():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    instance_ids = [instance['InstanceId'] for reservation in response['Reservations'] for instance in reservation['Instances']]
    
    logging.info("importing list of instances to be rightsized...\r")
    with open('resize_instances.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            inst_id, inst_type, app_id = row
            for instance_id in instance_ids:
                if instance_id == inst_id:
                    logging.info("instance match... \r")
                    if inst_type != instance['InstanceType']:
                        logging.info("checking instance type for change... \r")
                        with open('changed_instances.csv', mode='a') as changed_file:
                            csv_writer = csv.writer(changed_file)
                            csv_writer.writerow([inst_id, inst_type, instance['InstanceType'], app_id])
                        logging.info("instance written. \r")