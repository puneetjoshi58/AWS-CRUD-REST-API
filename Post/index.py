
from custom_encoder import CustomEncoder
import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

PostMethod = 'POST'
PostPath = '/data_post'

def handler(event,context):
    
    
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    
    if httpMethod == PostMethod and path == PostPath:
        response = CreateName(json.loads(event['body']))
    else :
        response = buildResponse(404, 'Not Found')
        
    return response

def CreateName(requestBody):
    
    client = boto3.resource('dynamodb')
    table = client.Table('user_data')
    
    try:
        table.put_item(Item=requestBody)
        body={
            'Operation': 'CREATE',
            'Message' : 'SUCCESS',
            'Item' : requestBody
        }
        return buildResponse(200, body)
    except:
        logger.exception('TIP: Check connection to the database')
        
def buildResponse(statusCode, body=None):
    response={
    'statusCode' : statusCode,
    'headers':{
         'Content-Type ': 'application/json',
         'Access-Control-Allow-Origin': '*'
         
    }    
    }
    
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)
        
    return response
        
        