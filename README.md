# PS_DataOps_Project

## Setup

### Configuration

Use the `template_airflow.cfg` file to create the necessary `airflow.cfg` file in the `/docker/airflow/` sub-directory. Place your preferred email credentials into this new file under the [smtp] section.

Similarly, necessary AWS credentials are stored in a `/dag/project_config.py` file. You can recreate this using the `template_project_config.py` file in this repository.

## Project - Part 1 (Required)

Prompt:
> Coindesk has a public facing REST API that provides bitcoin price data (https://api.coindesk.com/v1/bpi/currentprice.json). 
Design a system to pull data from the API every 5 minutes and land each data pull as a file in an AWS S3 Bucket. 
Prepare a short presentation or diagram to share with us during your interview so that you can walk us through your design.


The system that I have is built using Airflow, Docker, Python, and an AWS S3 Bucket. When scheduled, the Airflow DAG `file_to_S3` (1) hits the coinbase API every five minutes, (2) writes the results into an AWS S3 bucket, and (3) sends a confirmation to my personal email.

**Airflow GUI:**

![](https://github.com/JacobwLyman/take_home_interviews/blob/master/Pluralsight/dataops_engineer/images/airflow.png)

**S3 Bucket:**

![](https://github.com/JacobwLyman/take_home_interviews/blob/master/Pluralsight/dataops_engineer/images/S3_bucket.PNG)

**Confirmation Emails:**

![](https://github.com/JacobwLyman/take_home_interviews/blob/master/Pluralsight/dataops_engineer/images/emails.PNG)

**Email Message:**

![](https://github.com/JacobwLyman/take_home_interviews/blob/master/Pluralsight/dataops_engineer/images/confirmation_message.png)

## Project - Part 2 (As you are able)

```
Include in your presentation or diagram:
- Python code showing how you would pull data from the API and load it into an AWS S3 Bucket.
- Terraform or CloudFormation code showing how you would set up the infrastructure your code would run on in the AWS cloud.
- Include code that shows how you would orchestrate your code to retrieve data from the API every 5 minutes.
```

Please see above images, along with the code and setup instructions of this repository.
