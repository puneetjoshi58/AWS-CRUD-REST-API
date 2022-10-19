import json
import boto3
import logging
from custom_encoder import CustomEncoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)

PutMethod = 'PUT'
PutPath= '/data_put'

def handler(event, context):
    
    
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    
    if httpMethod == PutMethod and path == PutPath:
        response = PutName(json.loads(event['body']))
        
    else :
        response = buildResponse(404, 'NotFound')
        
    return response
        
        
def PutName(requestBody):
    
    client_dynamo=boto3.resource('dynamodb')
    table=client_dynamo.Table('user_data')
    
    try:
        table.put_item (Item = requestBody)
        
        body = {
                'Operation' : 'PUT',
                'Message' : 'SUCCESS',
                'Item' : requestBody
            }
        return buildResponse(200,body)
        
    except:
         logger.exception('TIP: Check for the correct Primary Key')
    
        
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