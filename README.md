# S3 Cost and Usage Explorer
## Retrieve, visualize, and evaluate S3 usage

### Files:  
main.py - The main file that drives the application.  
converter.py - Helper functions for converting a json to tabular data.  
usage.csv - Usage data transformed and stored as a csv.
usage.json - S3 usage data retrieved from AWS cost explorer.
usage.jpg - Time series of monthly S3 costs.
example_data - Sample S3 usage data that can be used to test functionality without connecting to an AWS account.

### Requirements:
An AWS account and S3 bucket.  
A IAM user with get/put/list S3 and cost explorer permissions.  
Pre-configured profile and access keys.

### Recommendations:
Host the python script on an EC2 instance with a Linux OS.  
Establish rotating access keys and allow developers to remotely SSH into the EC2 instance.  
Store model outputs in S3.  
Connect QuickSight to S3 data and create a monitoring and reporting dashboard.
