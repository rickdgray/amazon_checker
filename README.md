# Amazon Preorder Availability Checker
This script is a work in progress! Do not rely on it!

This python script will poll the Amazon product API to check if an item exists; if it does, it will send you a text message every 2 seconds! Convenient to wake you up if it becomes available at 2AM. To be clear, the Amazon website may list an item, but the API will report that an ASIN could not be found if the item is not available for purchase. That is the basis for how this script works.

Also, this is not intended to be a watchdog for sales or discounts, though it may be used in that regard. For such a feature, something like camelcamelcamel.com is better suited.

Setup:

To make this code work, you must first acquire three things:

Amazon product advertising API access key and it's associated secret key

An Amazon associate tag

AWS User Token/Key and it's associated secret key

The product API access key, secret key, and associate tag can easily be set up by the instructions on this page:

http://docs.aws.amazon.com/AWSECommerceService/latest/GSG/GettingStarted.html

The AWS user access key and secret key can be set up by following this:

http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey

Next, run

pip install awscli

This will install the AWS CLI. From a terminal/command prompt, run

aws configure

It will ask four questions. Give it the AWS access key and secret key, a default region (Text messaging is only available in some regions. I recommend 'us-east-1') and ignore the last question.

This will create config files in .aws folder in your user or home directory.

Take the product advertising access key and secret key and the associate tag, and put them into the python script at the top.

Also change the +15555555555 phone number to your phone number.

The next step is to set up SNS. This is the AWS service for sending text messages. You can set this up here:

https://console.aws.amazon.com/mobilehub/home?region=us-east-1#/

Create a basic project; you don't need to make any campaigns or sections or anything else. When you have it created, it should allow you to download a awsconfiguration.json file. Place this file in the root of the project folder (next to amazon_checker.py).

Running:

Simply run make to run the script! If you don't have make installed you may also run

python amazon_checker.py