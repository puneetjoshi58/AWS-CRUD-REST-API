import json
import boto3
import logging
from custom_encoder import CustomEncoder

#the logger retrives information about the event passed to the handler

logger = logging.getLogger()
logger.setLevel(logging.INFO)    

#initialising method name and path 

DeleteMethod = 'DELETE'
DeletePath= '/data_delete'

#def of the lambda function

def handler(event,context):
    
    
    logger.info(event)
    httpMethod = event['httpMethod']        
    path = event['path']
    
    if httpMethod == DeleteMethod and path == DeletePath:
        
        #requestBody stores the raw json body sent by the user as input using the api 
        
        requestBody = json.loads(event['body'])
        response = DeleteName(requestBody['Name'])        
        
    else :
        response = buildResponse(404, 'NotFound')
        
    return response

def DeleteName(Name):
    
    #linking the DDB to boto3
    
    client = boto3.resource('dynamodb')                 
    table= client.Table('user_data')
    
    try:
        
        # Deleting by the Key 'Name'
        
        response = table.delete_item(                   
            Key={
                'Name': Name
                },
            ReturnValues = 'ALL_OLD'
        )
        
        body = {                                        
            'Operation' : 'DELETE',
            'Message' : 'SUCCESS',
            'DeletedItem' : response
        }
        
        #returns 200 status code for successful execution
         
        return buildResponse(200 , body)               
        
        
    except :
        logger.exception('TIP: Check if Item exists in table')
                
                
#def to return data to the api in the required format 

def buildResponse(statusCode, body=None):                   
    response={
    'statusCode' : statusCode,
    'headers':{
         'Content-Type ': 'application/json',             
         
         #enabling CORS
         
        'Access-Control-Allow-Origin': '*'                
         
    }    
    }
    
    if body is not None:
        
        # returning a string equivalent of the json object                                    
        response['body'] = json.dumps(body, cls=CustomEncoder)
        
    return response
        