#!/usr/bin/env python3

import aws_cdk as cdk

from aws_crud_rest_api.aws_crud_rest_api_stack import AwsCrudRestApiStack


app = cdk.App()
AwsCrudRestApiStack(app, "aws-crud-rest-api")

app.synth()
