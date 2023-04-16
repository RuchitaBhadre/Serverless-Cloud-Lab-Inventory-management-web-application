import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime,timedelta


class dynamoManager:

    def __init__(self,key_id="AKIARQKRVO4SRFYI4KPJ",secret_key="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",region="us-east-1"):
        self.key_id=key_id
        self.secret_key=secret_key
        self.region=region
        #self.id=self.check_id()

    def check_id(self):
        self.start_instance()
        response = self.dynamo.scan(TableName='Devices1')
        start=[]
        for items in response['Items']:
            start.append(int(items['Device Id']['N']))
        start.sort()
        if(start==[]):
            return 0
        return start.pop()

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
            table1=self.dynamo_.Table('Rent_Logs')
            new_item=table.put_item(
            Item={
                'Username':Username,
                'Email_Id':Email,
                'Password':Password,
                }
            )
            new_item1 = table1.put_item(
                Item={
                    'Username': Username,
                    'Email Id': Email,
                    'Title1':"None",
                    'Title2': "None",
                    'Issue1': "None",
                    'Issue2': "None",
                    'Return1':"None",
                    'Return2': "None",


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

    def delete_item(self, Username, Email):
        self.start_instance()
        check = self.get_item(Username, Email)
        if (check[0] != []):
            table = self.dynamo_.Table('Registered_users')
            table.delete_item(
                Key={
                    'Username': Username,
                    #'Email_Id': Email,
                }
            )
            table1 = self.dynamo_.Table('Rent_Logs')
            table1.delete_item(
                Key={
                    'Username': Username,
                    # 'Email_Id': Email,
                }
            )
            return ("Done")
        else:
            return ("Not Done")


    def add_device(self,Title,MFD,Units,Brand):
        self.start_instance()
        check=self.get_specific_item(Title)
        if(check == True):
            table=self.dynamo_.Table('Devices1')
            new_item=table.put_item(
            Item={
                'Device_Title':Title.upper(),
                #'Device Id':int(self.check_id())+1,
                'Brand' : Brand.upper(),
                'MFD':MFD,
                'Units':int(Units),
                }
            )
            return (True)
        else:
            return (False)

    def delete_device(self, Title):
        self.start_instance()
        table = self.dynamo_.Table('Devices1')
        table.delete_item(
            Key={
                'Device_Title': Title,

            }
        )

    def modify_device(self, Title, Brand, MFD, Units):
        self.start_instance()
        check = self.get_specific_item(Title)
        if (check == False):
            table = self.dynamo_.Table('Devices1')
            table.update_item(
                Key={
                    'Device_Title': Title,

                },
                UpdateExpression='SET Brand = :val1, MFD = :val2, Units = :val3',
                ExpressionAttributeValues={
                    ':val1': Brand,
                    ':val2':MFD,
                    ':val3': int(Units)
                }
            )
            return (True)
        else:
            return (False)

    """
    def get_all_devices(self):
        self.start_instance()
        response = self.dynamo.scan(
                TableName='Devices1'
            )
        return response['Items']
        """

    def get_specific_item(self,Title):
        self.start_instance()
        table=self.dynamo_.Table('Devices1')
        response=table.query(
            KeyConditionExpression=Key('Device_Title').eq(Title)
            )
        if(response['Items']==[]):
            return (True)
        else:
            return (False)

    def searching_devices(self, keyword):
        self.start_instance()
        table = self.dynamo_.Table('Devices1')
        response = table.scan(
            FilterExpression=Attr('Device_Title').contains(keyword) | Attr('Device_Title').contains(keyword.upper())
        )
        if (response['Items'] == []):
            return []
        else:
            return response['Items']


    def decreasecopy(self,Title,Units):
        self.start_instance()
        current_copies=int(Units)-1
        table=self.dynamo_.Table('Devices1')
        new_item1=table.update_item(
                Key={
                    'Device_Title':Title,
                    #'Brand':Brand,

                },
                UpdateExpression='SET Units = :val1',
                ExpressionAttributeValues={
                    ':val1': current_copies
                }
                )

    def increasecopy(self,Title,Units):
        self.start_instance()
        current_copies=int(Units)+1
        table=self.dynamo_.Table('Devices1')
        new_item1=table.update_item(
                Key={
                    'Device_Title':Title,
                    #'Brand' : Brand,

                },
                UpdateExpression='SET Units = :val1',
                ExpressionAttributeValues={
                    ':val1': current_copies
                }
                )


    def RentingDevice(self,username,Title,Brand,Units,IDate,RDate):
        self.start_instance()
        if(int(Units)<=0):
            return("No Device")
        Email=self.get_item(username,Email="")
        table=self.dynamo_.Table('Rent_Logs')
        response=table.query(
            KeyConditionExpression=Key('Username').eq(username)
            )
        number=1
        try:
            if(response['Items'][0]['Title1']=='None'):
                self.decreasecopy(Title,Units)
                statement='SET Title'+str(number)+' = :val1,'+'Issue'+str(number)+' = :val2,'+'Return'+str(number)+' = :val3'
                rest=table.update_item(
                                Key={
                                    'Username':username,
                                    #'Email Id':Email[0][0]['Email_Id']
                                },
                                UpdateExpression=statement,
                                ExpressionAttributeValues={
                                    ':val1': Title,
                                    ':val2': IDate,
                                    ':val3':RDate
                                }
                            )
                return("Done")
            elif(response['Items'][0]['Title1']!=None):
                if(response['Items'][0]['Title1'] == Title):
                    return ("Already There")
                try:
                    if(response['Items'][0]['Title2']=='None'):
                        self.decreasecopy(Title,Units)
                        number+=1
                        statement='SET Title'+str(number)+' = :val1,'+'Issue'+str(number)+' = :val2,'+'Return'+str(number)+' = :val3'
                        rest=table.update_item(
                                        Key={
                                            'Username':username,
                                            #'Email Id':Email[0][0]['Email_Id']
                                        },
                                        UpdateExpression=statement,
                                        ExpressionAttributeValues={
                                            ':val1': Title,
                                            ':val2': IDate,
                                            ':val3':RDate
                                        }
                                    )
                        return("Done")
                    elif(response['Items'][0]['Title2']!=None):
                        return("Not Done")
                except:
                    self.decreasecopy(Title,Units)
                    number+=1
                    statement='SET Title'+str(number)+' = :val1,'+'Issue'+str(number)+' = :val2,'+'Return'+str(number)+' = :val3'
                    rest=table.update_item(
                                Key={
                                    'Username':username,
                                    #'Email Id':Email[0][0]['Email_Id']
                                },
                                UpdateExpression=statement,
                                ExpressionAttributeValues={
                                    ':val1': Title,
                                    ':val2': IDate,
                                    ':val3':RDate
                                }
                            )
                    return("Done")
        except:
            self.decreasecopy(Title,Units)
            statement='SET Title'+str(number)+' = :val1,'+'Issue'+str(number)+' = :val2,'+'Return'+str(number)+' = :val3, Title2 = :val4, Issue2 = :val5, Return2 = :val6'
            if(response['Items']==[]):
                rest=table.update_item(
                                Key={
                                    'Username':username,
                                    #'Email Id':Email[0][0]['Email_Id']
                                },
                                UpdateExpression=statement,
                                ExpressionAttributeValues={
                                    ':val1': Title,
                                    ':val2': IDate,
                                    ':val3':RDate,
                                    ':val4':"None",
                                    ':val5':"None",
                                    ':val6':"None"
                                }
                            )
            return("Done")

    def renew(self, username, Title, RDate):
        self.start_instance()
        table = self.dynamo_.Table('Rent_Logs')
        response = table.query(
            KeyConditionExpression=Key('Username').eq(username)
        )
        if (response['Items'][0]['Title1'] == Title):
            new_date = (datetime.strptime(response['Items'][0]['Return1'].replace("-", ""),
                                          "%Y%m%d").date() + timedelta(days=int(RDate)))
            rest = table.update_item(
                Key={
                    'Username': username,
                    #'Email Id': response['Items'][0]['Email Id']
                },
                UpdateExpression='SET Return1 = :val1',
                ExpressionAttributeValues={
                    ':val1': str(new_date)
                }
            )
            return ("Done")
        elif (response['Items'][0]['Title2'] == Title):
            new_date = (datetime.strptime(response['Items'][0]['Return2'].replace("-", ""),
                                          "%Y%m%d").date() + timedelta(int(RDate)))
            rest = table.update_item(
                Key={
                    'Username': username,
                    #'Email Id': response['Items'][0]['Email Id']
                },
                UpdateExpression='SET Return2 = :val1',
                ExpressionAttributeValues={
                    ':val1': str(new_date)
                }
            )
            return ("Done")
        else:
            return ("Device not rented")

    def get_all_rental(self):
        self.start_instance()
        response = self.dynamo.scan(
            TableName='Rent_Logs'
        )
        return response['Items']

    def get_email_item(self, Username):
        self.start_instance()
        table = self.dynamo_.Table('Rent_Logs')
        response = table.query(
            KeyConditionExpression=Key('Username').eq(Username)
        )
        return [response['Items'], 'Email Id']
    def get_email1_item(self, Username):
        self.start_instance()
        table = self.dynamo_.Table('Rent_Logs')
        response = table.query(
            KeyConditionExpression=Key('Username').eq(Username)
        )
        return response['Items'][0]['Email Id']

    def returned_device(self, Username, Title):
        self.start_instance()
        table = self.dynamo_.Table('Rent_Logs')
        response = table.query(
            KeyConditionExpression=Key('Username').eq(Username)
        )
        if (response['Items'] == []):
            return ("User Invalid")
        Email = response['Items'][0]['Email Id']
        if (response['Items'][0]['Title1'] == Title):
            device_info = self.searching_devices(Title)
            self.increasecopy(Title, device_info[0]['Units']) #check this for whats being returned from device info
            rest = table.update_item(
                Key={
                    'Username': Username,
                    #'Email Id': Email
                },
                UpdateExpression='SET Title1 = :val1,Issue1 = :val2,Return1 = :val3',
                ExpressionAttributeValues={
                    ':val1': "None",
                    ':val2': "None",
                    ':val3': "None"
                }
            )
            return ("Done")
        elif (response['Items'][0]['Title2'] == Title):
            device_info = self.searching_devices(Title)
            self.increasecopy(Title, device_info[0]['Units'])
            rest = table.update_item(
                Key={
                    'Username': Username,
                    #'Email Id': Email
                },
                UpdateExpression='SET Title2 = :val1,Issue2 = :val2,Return2 = :val3',
                ExpressionAttributeValues={
                    ':val1': "None",
                    ':val2': "None",
                    ':val3': "None"
                }
            )
            return ("Done")
        else:
            return ("Incorrect Device")

