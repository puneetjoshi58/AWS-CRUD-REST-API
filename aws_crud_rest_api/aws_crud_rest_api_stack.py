from constructs import Construct
from aws_cdk import (
    Stack,
   aws_iam as _iam,
   aws_dynamodb as _dynamodb,
   aws_lambda as _lambda,
   aws_apigateway as _apigateway
   
   
)


class AwsCrudRestApiStack(Stack):
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        user_data = _dynamodb.Table(self,id='Name',table_name='user_data',
                                  partition_key= _dynamodb.Attribute(name = 'Name', type= _dynamodb.AttributeType.STRING))
        
        enable_CRUDApi = _iam.Role(self, "enable_CRUDApi",
            assumed_by= _iam.ServicePrincipal("lambda.amazonaws.com")
            )
        
        enable_CRUDApi.add_managed_policy(_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayInvokeFullAccess"))
        enable_CRUDApi.add_managed_policy(_iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"))
        enable_CRUDApi.add_managed_policy(_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayAdministrator"))
        enable_CRUDApi.add_managed_policy(_iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambda_FullAccess"))
        enable_CRUDApi.add_managed_policy(_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"))
        
        get_user_data = _lambda.Function(self, id='get_user_data',runtime= _lambda.Runtime.PYTHON_3_9,
                                     handler='index.handler',
                                     code=_lambda.Code.from_asset('GetItem'),
                                     role=enable_CRUDApi
                                     )
        
        put_user_data = _lambda.Function(self, id='put_user_data',runtime= _lambda.Runtime.PYTHON_3_9,
                                     handler='index.handler',
                                     code=_lambda.Code.from_asset('PutItem'),
                                     role=enable_CRUDApi
                                     )
        
        delete_user_data = _lambda.Function(self, id='delete_user_data',runtime= _lambda.Runtime.PYTHON_3_9,
                                     handler='index.handler',
                                     code=_lambda.Code.from_asset('DeleteItem'),
                                     role=enable_CRUDApi
                                    )
        
        post_user_data = _lambda.Function(self, id='post_user_data',runtime= _lambda.Runtime.PYTHON_3_9,
                                     handler='index.handler',
                                     code=_lambda.Code.from_asset('Post'),
                                     role=enable_CRUDApi
                                     )
        
        check_api_health = _lambda.Function(self, id='check_api_health',runtime= _lambda.Runtime.PYTHON_3_9,
                                     handler='index.handler',
                                     code=_lambda.Code.from_asset('Health'),
                                     role=enable_CRUDApi
                                     )
        
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
        
       