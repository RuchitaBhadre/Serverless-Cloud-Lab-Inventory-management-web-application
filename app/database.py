import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime,timedelta

class dynamoManager:

    def __init__(self,key_id="AKIARQKRVO4SRFYI4KPJ",secret_key="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",region="us-east-1"):
        self.key_id=key_id
        self.secret_key=secret_key
        self.region=region
        #self.id=self.check_id()



    def start_instance(self):
        self.dynamo = boto3.client('dynamodb',
                    aws_access_key_id=self.key_id,
                    aws_secret_access_key=self.secret_key,
                    region_name=self.region
                     )
        self.dynamo_=boto3.resource('dynamodb',
                    aws_access_key_id=self.key_id,
                    aws_secret_access_key=self.secret_key,
                    region_name=self.region
                    )



    def add_item(self,Username,Email,Password):
        self.start_instance()
        check=self.get_item(Username,Email)
        if(check[0] == []):
            table=self.dynamo_.Table('Registered_users')
            new_item=table.put_item(
            Item={
                'Username':Username,
                'Email_Id':Email,
                'Password':Password,
                }
            )
            return [True]
        else:
            return check



    def get_item(self,Username,Email):
        self.start_instance()
        table=self.dynamo_.Table('Registered_users')
        response=table.query(
            KeyConditionExpression=Key('Username').eq(Username)
            )
        if(response['Items']==[]):
            response=table.scan(
                FilterExpression=Attr('Email_Id').eq(Email)
            )
            return [response['Items'],'Email Id']
        else:
            return [response['Items'],'Username']