  
import json
import boto3
from  pprint import pprint
import time

def lambda_handler(event, context):
  cloud_break_count = 0 
  tagged_now =   0
  cant_tag   =   0
  alrdy_tagged = 0
  all_ec2_count = 0
  
  regions = ["eu-west-1","eu-west-2","us-east-1"]
  for region in regions:
    ec2_resource = boto3.resource('ec2', region_name=region)
    instances = ec2_resource.instances.all()
    
    for instance in instances:

      cloud_break_count += 1
      if (  cloud_break_count == 5 ):
          
      
        time.sleep(1)
        cloud_break_count = 0 
            
            
      all_ec2_count += 1
      instance_id = instance.id
      #print(instance_id)
      flag = 0
        
      if ( len(instance.tags) != 0 ):
        for tag in instance.tags:
          if ( tag['Key'] == 'map-migrated' ):
              
            flag = 1
            alrdy_tagged += 1
            print(tag)
              
                    
                
      if ( flag == 0  ):
        try:
          ec2 = boto3.client('ec2')
          response = ec2.create_tags(
          DryRun=False,
          Resources=[instance_id],
          Tags=[{
          'Key': 'map-migrated',
          'Value': 'd-server-00a0posufm7nfr'}])
          
          tagged_now += 1
                
                
        except Exception as e:
          print(e)
          cant_tag += 1
                
                
  print('all ec2  count',all_ec2_count)
  print('already tagged count' ,alrdy_tagged )
  print('tagged from this attempt',tagged_now)
  print('refused to tag',cant_tag )