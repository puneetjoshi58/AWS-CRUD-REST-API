import json
import boto3
import logging
from custom_encoder import CustomEncoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)    

DeleteMethod = 'DELETE'
DeletePath= '/data_delete'


def handler(event,context):
    
    
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    
    if httpMethod == DeleteMethod and path == DeletePath:
        requestBody = json.loads(event['body'])
        response = DeleteName(requestBody['Name'])
        
    else :
        response = buildResponse(404, 'NotFound')
        
    return response

def DeleteName(Name):
    client = boto3.resource('dynamodb')
    table= client.Table('user_data')
    try:
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
        return buildResponse(200 , body)
        
        
    except :
        logger.exception('TIP: Check if Item exists in table')
                
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
        