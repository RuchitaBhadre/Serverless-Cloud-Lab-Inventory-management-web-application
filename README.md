
# **Application Description:  ECE TOOLS Lab Inventory**

We developed a Cloud Lab Inventory management project that manages and stores devices’ information electronically according to users needs. The system helps both users and Lab Inventory admin to keep a constant track of all the devices available in the Lab Inventory. It allows both the admin and the student to search for the desired device electronically. This system reduces manual work to a great extent and allows smooth flow of Lab Inventory activities by removing chances of errors in the details. The Cloud Lab Inventory excludes the use of paper work by managing all the devices information electronically. Admin can keep updating the system by providing the new devices arrival in system and their availability thus users need not to go to the Lab Inventory for issuing purposes. Our web application for Lab Inventory management can be divided into two modules. One module is for Administrators of the Lab Inventory and the other module is for the users.

The users can register themselves and navigate through their user homepage to issue, rent and renew their devices. Additionally, the user can check out the contact us page for any queries and will be registered in the Lab Inventory mailing system for updates. The administrator has complete control of the admin page and various functionalities present in their homepage. To develop this, AWS services like AWS Lambda, Zappa, S3, DynamoDB, SES have been used.

**Use Description:**

The web application provides the following three main features through the web interface:



|<p>**Registration page** : </p><p></p><p>Users have to register themselves into the system to create an account. After registering successfully, they can then login into the system by entering their username and their password.</p>|![](images/Aspose.Words.3eeba9df-3375-4898-a3b6-dcf8c4bf8b8d.002.png)|
| :- | :-: |
|<p>**Login page:**</p><p></p><p>This page provides authentication to access the webpage both for the customer and the employee separately after registration. </p>|![](images/Aspose.Words.3eeba9df-3375-4898-a3b6-dcf8c4bf8b8d.003.png)|
|<p>**User Home page:** </p><p>This page is accessible by the user and the user would be able to view all the available devices in the Lab Inventory or search for them which on clicking would take them directly to the rent page where they can rent the device of their choice. The user also has an option to renew their date of return for the devices they have.They can contact the admin through the contact us page for any queries. </p>|![](images/Aspose.Words.3eeba9df-3375-4898-a3b6-dcf8c4bf8b8d.004.png)|
|<p>**Admin Home page**: </p><p>This page is accessible only to the admin and they can make use of the different functionalities available. Admin administers the system by adding or removing devices into and from the system respectively.The admin can update the details of the device, can view order for the devices and devices list available in the database. </p>|![](images/Aspose.Words.3eeba9df-3375-4898-a3b6-dcf8c4bf8b8d.005.png)|


**Application Architecture:** 

Our web application employs **Amazon DynamoDB,** a fully managed NoSQL database that leverages a key-value pair and document model for data storage. We specifically use three tables within DynamoDB: Devices1 (with the partition key as Device\_Title), Registered Users (with the partition key as Username), and Rent Logs (with partition keys as username). **AWS Lambda** is an event-driven, serverless computing platform that automatically manages computing resources in response to events. In our web application, we utilize Lambda functions to incorporate AWS SES functionality, which allows us to send emails to registered users when a particular event is triggered. For example, a Lambda function might be triggered when a user requests a device or utilizes the "contact us" page.

**Amazon SES** is a highly cost-effective, flexible, and scalable email service that enables users to send email securely, globally, and at a large scale. With AWS SES, we can send mail directly from within the application. Acting as an API front-end, the **API gateway** server processes incoming API requests, enforces throttling and security policies, routes requests to the back-end service, and finally returns the response back to the requester. Additionally, gateways often integrate with transformation engines to dynamically orchestrate and modify requests and responses. By utilizing **Zappa**, deploying a Flask application as an AWS Lambda function becomes simple and straightforward.

**User Module:** 

The users can register themselves and navigate through their user homepage to issue, rent and renew their devices. Additionally, the user can check out the contact us page for any queries and will be registered in the Lab’s mailing system for updates. 

**Admin Module:** 

The admin has the full authority to perform the functionalities present in the admin page. They can 

Delete User, Modify Device, Delete Device, Add Device, View User list, View Device list, Rent logs, 

Return Device

**Overall Architecture:**

![](images/Aspose.Words.3eeba9df-3375-4898-a3b6-dcf8c4bf8b8d.006.png)

**Lambda Architecture:**

![](images/Aspose.Words.3eeba9df-3375-4898-a3b6-dcf8c4bf8b8d.007.png)

**DynamoDB Architecture:**

![](images/Aspose.Words.3eeba9df-3375-4898-a3b6-dcf8c4bf8b8d.008.png)

**Cost Model:**

Assuming that at the outset of launching our app, there were about 50 individuals who frequented our site for purchases. Over time, this number grew exponentially such that after half a year, we had amassed roughly one million users. To determine the costs associated with our app, we utilized both AWS pricing documentation and the AWS price calculator, taking into account the specific services we employ. These services and their corresponding cost estimates are itemized below.

**AWS DynamoDB:**

We incur costs from DynamoDB based on the specific features we utilize, which include read requests, write requests, data storage, and data transfer. In our app, we rely on read and write requests, as well as data transfer and storage.

Data-storage: First 25 GB stored per month is free using the DynamoDB Standard table class. $0.25 per GB-month thereafter.

Monthly write cost (monthly): 26.39 USD

Upfront write cost (upfront): 180.00 USD

Data-transfer: AWS does not charge for data transfer between DynamoDB and other AWS services.

Considering there are 100 requests to write and read from 10 users for 1 month, with peak request up to 400 one-month estimation of DynamoDB is as shown below.

` `![](images/Aspose.Words.3eeba9df-3375-4898-a3b6-dcf8c4bf8b8d.009.png)

**API GATEWAY:**

Under the Amazon API Gateway free tier, we're afforded the ability to make a maximum of one million REST API calls, one million HTTP API calls, and send up to one million messages with 750,000 connection minutes for WebSocket APIs each month. These benefits are available for up to 12 months, after which fees will be assessed for any usage that exceeds these caps. 

To illustrate, consider the hypothetical scenario of 10 users who generate one million REST API requests in a given month; we can estimate the associated expenses as outlined below.

![](images/Aspose.Words.3eeba9df-3375-4898-a3b6-dcf8c4bf8b8d.010.png)

**AWS SES:** 

Suppose a single user sends 30 emails using an email client. Based on this assumption, the estimated cost for 10 users can be calculated as follows: If the application is hosted on EC2, Amazon will not charge anything for the first 62,000 emails sent per month, but will charge $0.10 for every 1,000 emails sent thereafter.

Assuming that 300 mails are sent to clients per month each or 10 GB and 50 emails are received every month each of 10 GB, the cost estimate for the month is as follows:

![](images/Aspose.Words.3eeba9df-3375-4898-a3b6-dcf8c4bf8b8d.011.png)

**AWS Lambda:**

To use AWS Lambda, you are charged based on the amount of requests made to your functions and the time your code takes to run. However, the AWS Lambda free tier allows for one million requests and 400,000 GB-seconds of compute time per month without charge.

Assuming there are 1,000,000 requests from 10 user for the month, one month estimation of Lambda is as shown below.

![](images/Aspose.Words.3eeba9df-3375-4898-a3b6-dcf8c4bf8b8d.012.png)

**After six months:** 

Assuming all the users are using our application frequently.


|**Service/Users**|**10 Users** |**1000 Users** |**1000,000 Users**|
| :-: | :-: | :-: | :-: |
|AWS DynamoDB|140\.28|1261\.024|660,132.95|
|Amazon API Gateway|21\.00|` `7,913.10|324,053.10 |
|AWS Simple Email Service|7\.44|24\.89|12,101.20|
|AWS Lambda|100|380|930|

**Below is the graphical representation of the data from table:**

![](images/Aspose.Words.3eeba9df-3375-4898-a3b6-dcf8c4bf8b8d.013.png)

**Performance Results:**


|**Latency Graph**|**Throughput Graph**|
| :- | :- |
|![](images/Aspose.Words.3eeba9df-3375-4898-a3b6-dcf8c4bf8b8d.014.png)|![](images/Aspose.Words.3eeba9df-3375-4898-a3b6-dcf8c4bf8b8d.015.png)|

Upon conducting a thorough analysis of our application's performance, we have observed an **average throughput of 77.9 hits per second**, with an **average response time of 62 milliseconds**. It is noteworthy that **90% of the responses** were processed within a **duration of 75 millisecond**s, indicating a satisfactory level of system responsiveness. Moreover, the **error rate** was observed to be a meager **0.44%**, thereby highlighting the **application's** **reliability and stability!**

