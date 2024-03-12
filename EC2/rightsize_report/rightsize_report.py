import boto3
import csv
from concurrent.futures import ThreadPoolExecutor

def check_ec2_instance(instance_id, instance_type, app_tag):
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-id', 'Values': [instance_id]}])
    
    for instance in instances:
        if instance.instance_type != instance_type:
            with open('changed_instances.csv', mode='a') as file:
                writer = csv.writer(file)
                writer.writerow([instance.id, instance.instance_type, app_tag])

def multithreaded_check_instances(csv_file):
    with open(csv_file, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        with ThreadPoolExecutor() as executor:
            for row in csv_reader:
                executor.submit(check_ec2_instance, row[0], row[1], row[2])

# Example usage
multithreaded_check_instances('instances_to_check.csv')