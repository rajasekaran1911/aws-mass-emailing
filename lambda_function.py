import boto3
import csv
import os

# AWS Clients
s3_client = boto3.client('s3')
ses_client = boto3.client('ses')

# Configurations
SENDER_EMAIL = "your-verified-email@example.com"  # Replace with your SES verified email
S3_BUCKET_NAME = "your-bucket-name"  # Replace with your actual S3 bucket name
SUBJECT = "Mass Email Notification"
BODY_TEXT = "This is an automated email using AWS Lambda and SES."

def lambda_handler(event, context):
    """Triggered when a file is uploaded to S3. Reads emails from CSV and sends them via SES."""
    
    try:
        # Print the full event to understand its structure
        print("🔹 Event received:", event)

        # Check if 'Records' key exists in the event
        if 'Records' not in event:
            print("❌ Error: Event does not contain 'Records'. Check S3 trigger setup.")
            return {"error": "Invalid event format", "event": event}

        # Extract bucket and file details
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']
        
        print(f"📂 Processing file {object_key} from bucket {bucket_name}")

        # Ensure Lambda processes only the expected bucket
        if bucket_name != S3_BUCKET_NAME:
            print(f"⚠️ Skipping file from unknown bucket: {bucket_name}")
            return {"status": "Skipped unknown bucket"}

        # Download file from S3
        local_path = f"/tmp/{object_key}"
        s3_client.download_file(bucket_name, object_key, local_path)
        
        print(f"✅ File downloaded to {local_path}")

        # Read CSV file and extract email addresses
        recipient_emails = []
        with open(local_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header
            for row in csv_reader:
                recipient_emails.append(row[0])  # Assuming first column contains emails

        print(f"📧 Found {len(recipient_emails)} email addresses")

        # Send emails via AWS SES
        for recipient in recipient_emails:
            try:
                print(f"🚀 Sending email to {recipient}")
                ses_client.send_email(
                    Source=SENDER_EMAIL,
                    Destination={'ToAddresses': [recipient]},
                    Message={'Subject': {'Data': SUBJECT}, 'Body': {'Text': {'Data': BODY_TEXT}}}
                )
                print(f"✅ Email sent to {recipient}")
            except Exception as e:
                print(f"❌ Error sending email to {recipient}: {e}")

        return {"status": "Emails sent successfully!"}

    except Exception as e:
        print(f"🔥 Unhandled exception: {e}")
        raise e  # Rethrow the error so it appears in CloudWatch logs
