
# Welcome to AWS_CRUD_RestAPI

This application enables the user to perform CRUD operations on a DynamoDB using AWS LambdaFunctions as the backend and AmazonAPIGateway as a REST frontend.

Trial
## Workings

a CDK app with an instance of a stack (`AwsCrudRestApiStack`) is created which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.


The stack instance contains the following
1. A DynamoDB Table called "user_data" with the partition key set to "Name" with attribute type STRING
2. A custom IAM Role "enable_CRUDApi" which contains AWS managed policies that allow exection of the app
3. 5 Lambda Functions each with their own asset files makes up the backend

        1.get_user_data : fetches item from the initialized DynamoDB with the 'GET' method through queryStringParameters and returns values in a JSON format
        
        2.put_user_data : Inserts and edits existing items into the initialized DynamoDB with the 'PUT' method through a raw JSON format Body and returns the values inserted
        
        3.delete_user_data: Identifies existing item from the DynamoDB by the ParitionKey ,removes them from the DB and returns the values erased
        
        4.post_user_data : Only inserts items into the initialized DynamoDB with the 'POST' method through a raw JSON format Body and returns the values inserted
        
        5.check_api_health : Checks for the health of the API and returns a StatusCode 200 if it is working
        
4. 5 APIs each having their respecting Methods that enable them to perfom the CRUD operations

==> The CustomEncoder is designed to check if an instanced passed to it is a decimal(Since values retured ny the DynamoDB are of Decimal Form) and convert it into float

==>The `cdk.json` file tells the CDK Toolkit what files are to be executed and the permissions required to do so this information is then passed onto AWS CloudFormation to execute the app.

==>This cdk.json file is updated everytime the (`cdk synth`) command is used to emit the synthesized CloudFormation template

==>The stack is deployed with the (`cdk deploy`) command from the "cdk.out" file which is created and updated with each (`cdk synth`) command 

## Setup

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .venv directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```
To Create a basic framework like the one this is based on use command 

```
$ cdk init sample app -language python
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.



## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

## Tips

==> Remeber to save files after changes 


==> Remeber to perform `cdk synth` on saved changes before deploying

Enjoy!
