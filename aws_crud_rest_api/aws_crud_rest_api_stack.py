from constructs import Construct
from aws_cdk import (
    Stack,
   aws_iam as _iam,
   aws_dynamodb as _dynamodb,
   aws_lambda as _lambda,
   aws_apigateway as _apigateway
   
   
)
# An instance of a stack (`AwsCrudRestApiStack`) is created which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.

class AwsCrudRestApiStack(Stack):
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # A DynamoDB Table called "user_data" with the partition key set to "Name" with attribute type STRING
        
        user_data = _dynamodb.Table(self,id='Name',table_name='user_data',
                                  partition_key= _dynamodb.Attribute(name = 'Name', type= _dynamodb.AttributeType.STRING))
        
        #A custom IAM Role "enable_CRUDApi" which contains AWS managed policies that allow exection of the app
        
        enable_CRUDApi = _iam.Role(self, "enable_CRUDApi",
            assumed_by= _iam.ServicePrincipal("lambda.amazonaws.com")
            )
        
        enable_CRUDApi.add_managed_policy(_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayInvokeFullAccess"))
        enable_CRUDApi.add_managed_policy(_iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"))
        enable_CRUDApi.add_managed_policy(_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayAdministrator"))
        enable_CRUDApi.add_managed_policy(_iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambda_FullAccess"))
        enable_CRUDApi.add_managed_policy(_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"))
        
        #fetches item from the initialized DynamoDB with the 'GET' method through queryStringParameters and returns values in a JSON format
        
        get_user_data = _lambda.Function(self, id='get_user_data',runtime= _lambda.Runtime.PYTHON_3_9,
                                     handler='index.handler',
                                     code=_lambda.Code.from_asset('GetItem'),
                                     role=enable_CRUDApi
                                     )
        
        #Inserts and edits existing items into the initialized DynamoDB with the 'PUT' method through a raw JSON format Body and returns the values inserted
        
        put_user_data = _lambda.Function(self, id='put_user_data',runtime= _lambda.Runtime.PYTHON_3_9,
                                     handler='index.handler',
                                     code=_lambda.Code.from_asset('PutItem'),
                                     role=enable_CRUDApi
                                     )
        
        #Identifies existing item from the DynamoDB by the ParitionKey ,removes them from the DB and returns the values erased
        
        delete_user_data = _lambda.Function(self, id='delete_user_data',runtime= _lambda.Runtime.PYTHON_3_9,
                                     handler='index.handler',
                                     code=_lambda.Code.from_asset('DeleteItem'),
                                     role=enable_CRUDApi
                                    )
        
        #Only inserts items into the initialized DynamoDB with the 'POST' method through a raw JSON format Body and returns the values inserted
        
        post_user_data = _lambda.Function(self, id='post_user_data',runtime= _lambda.Runtime.PYTHON_3_9,
                                     handler='index.handler',
                                     code=_lambda.Code.from_asset('Post'),
                                     role=enable_CRUDApi
                                     )
        
        #Checks for the health of the API and returns a StatusCode 200 if it is working
        
        check_api_health = _lambda.Function(self, id='check_api_health',runtime= _lambda.Runtime.PYTHON_3_9,
                                     handler='index.handler',
                                     code=_lambda.Code.from_asset('Health'),
                                     role=enable_CRUDApi
                                     )
        
        # 5 APIs each having their respecting Methods that enable them to perfom the CRUD operations
        
        Api_Health = _apigateway.LambdaRestApi(self,id='api_health',rest_api_name='healthApi',handler = check_api_health)
        api_health = Api_Health.root.add_resource('api_health')
        api_health.add_method('GET')
        
        Data_Put = _apigateway.LambdaRestApi(self,id='data_put',rest_api_name='putApi',handler = put_user_data)
        data_put = Data_Put.root.add_resource('data_put')
        data_put.add_method('PUT')
        
        Data_Get = _apigateway.LambdaRestApi(self,id='data_get',rest_api_name='getApi',handler = get_user_data)
        data_get = Data_Get.root.add_resource('data_get')
        data_get.add_method('GET')
        
        Data_Delete = _apigateway.LambdaRestApi(self,id='data_delete',rest_api_name='deleteApi',handler = delete_user_data)
        data_delete = Data_Delete.root.add_resource('data_delete')
        data_delete.add_method('DELETE')
        
        Data_Post = _apigateway.LambdaRestApi(self,id='data_post',rest_api_name='postApi',handler = post_user_data )
        data_post = Data_Post.root.add_resource('data_post')
        data_post.add_method('POST')
        
       