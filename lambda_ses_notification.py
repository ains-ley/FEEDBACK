import boto3
import json

def lambda_handler(event, context):
    ses = boto3.client('ses')
    
    # These values should come from Glue or another source
    recipient_email = event['recipient_email']
    document_name = event['document_name']
    entity_list = event['entity_list']
    review_link = event['review_link']
    
    body = f"""Dear Reviewer,

A new data lineage model has been extracted from the document titled:

    {document_name}

The system has identified the following:
- Entities: {', '.join(entity_list)}
- Relationships and Keys
- Business rules and metadata

Please review and confirm the proposed structure. You can view the lineage model and submit feedback using the link below:

Review Now: {review_link}

If approved, this lineage will be promoted to the Gold layer and registered in the Data Catalog.

Best regards,
Data Lineage Automation System.
"""

    response = ses.send_email(
        Source='noreply@yourdomain.com',
        Destination={'ToAddresses': [recipient_email]},
        Message={
            'Subject': {'Data': '[ACTION REQUIRED] Review New Lineage Extracted from Business Document'},
            'Body': {'Text': {'Data': body}}
        }
    )
    
    return {'statusCode': 200, 'body': 'Notification sent', 'sesMessageId': response['MessageId']}
