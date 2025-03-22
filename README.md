AWS Lambda Mass Emailing Project

This project automates mass email sending using AWS Lambda, S3, and SES. When a CSV file containing email addresses is uploaded to an S3 bucket, a Lambda function reads the file and sends emails using Amazon Simple Email Service (SES).

🚀 Features
- ✅ Upload CSV file to S3 to trigger emails
- ✅ AWS Lambda reads and processes the file
- ✅ Uses AWS SES to send emails to verified addresses
- ✅ Scalable and cost-effective email solution

🛠️ Technologies Used
- AWS Lambda
- AWS S3 (Simple Storage Service)
- AWS SES (Simple Email Service)
- Python (Boto3 SDK)

📂 Project Structure
aws-mass-emailing/
│── lambda_function.py  
│── requirements.txt    
│── README.md           
│── .gitignore          
│── emails_sample.csv  
│── cloudformation.yaml 
│── terraform/          
└── venv/     

📧 Notes
SES Sandbox Mode: You can only send emails to verified addresses.
To send emails to unverified users, request SES production access.
Ensure IAM permissions are correctly set for S3 and SES.

📝 License
This project is licensed under the MIT License.

👨‍💻 Author
Rajasekaran J B         
