from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import boto3

app = FastAPI()
templates = Jinja2Templates(directory ="/Users/shaikim/Desktop/cloud_projects/AWS")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/Instances")
def get_Instances():
    ec2 = boto3.client("ec2", region_name= 'us-east-1')
    response = ec2.describe_instances()
    instances = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_info = {
                "InstanceId" : instance["InstanceId"],
                "InstanceType" : instance["InstanceType"],
                "State" : instance["State"]["Name"]
            }
            instances.append(instance_info)
    print("Instances:", instances)
    return {"instances": instances}


@app.get("/Buckets")
def get_Buckets():
    s3 = boto3.client("s3",region_name = 'us-east-1')
    response = s3.list_buckets()
    buckets = []
    for bucket in response['Buckets']:
        bucket_info = {
            "Name" : bucket['Name'],
            "BucketCreationDate" : bucket["CreationDate"]
        }
        buckets.append(bucket_info)
    print("Buckets:", buckets)
    return {"buckets": buckets}

@app.get("/CostExplorer")
def get_cost():
    costs = boto3.client('ce')
    
    response = costs.client.get_cost_and_usage(
        TimePeriod={
            'Start': '2024-04-01',
            'End': '2024-04-30'
        },
        Granularity='Monthly',
        Filter = {
                'CostCategories' : {
                    'Key': 'Service',
                    'Values' : ['AmazonEC2','AmazonS3']
                }      
        },
        Metrics=['BlendedCost'],
    )
    cost_data = response['ResultsByTime'][0]['Total']['BlendedCost']['Amount']
    





