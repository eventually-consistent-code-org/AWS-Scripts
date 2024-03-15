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

ec2 = boto3.resource('ec2')

awsinst_id = []
awsinst_type = []

logging.info("importing ec2 data from aws... \r")
for instance in ec2.instances.all():
    awsinst_id.append(instance.id)
    awsinst_type.append(instance.instance_type)

inst_id = []
inst_type = []
app_id = []
logging.info("importing from rightsizing recommendations csv... \r")
with open('resize_instances.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        inst_id.append(row[0])
        inst_type.append(row[1])
        app_id.append(row[2])
logging.info("comparing instance types \r")
for i in range(len(awsinst_id)):
    logging.info("aws instance: %s", awsinst_id)
    if awsinst_id[i] in inst_id:
        index = inst_id.index(awsinst_id[i])
        if awsinst_type[i] != inst_type[index]:
            print(f"Instance ID: {awsinst_id[i]}, Old Instance Type: {inst_type[index]}, New Instance Type: {awsinst_type[i]}, App ID: {app_id[index]}")
        else:
            print(f"instance is unchanged")