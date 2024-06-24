import boto3
from botocore.exceptions import ClientError
import re
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # Initialize S3 and SES clients
    s3_client = boto3.client('s3')
    ses_client = boto3.client('ses', region_name='us-east-1')

    # S3 bucket and file details
    BUCKET_NAME = 'metric-test-01'

    # List objects in the specified S3 bucket
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': f"Error fetching objects from S3 bucket: {e}"
        }
        
    # Get today's date
    today = datetime.today()
    # Subtract one day
    yesterday = today - timedelta(days=1)
    todays_date = today.strftime("%d %B %Y")
    latest_date_str = yesterday.strftime('%Y-%-m-%d')
    print(f"Today's date: {todays_date}")
    print(f"Yesterday's date: {latest_date_str}")
    
    # Formulate the folder key for the latest date
    folder_prefix = latest_date_str + '/'
    print(f"Searching for files in folder: {folder_prefix}")
    
    # Example list of patterns
    patterns = [
        fr'{re.escape(folder_prefix)}backend_to_obd-(\d+)\.csv',
        fr'{re.escape(folder_prefix)}backend_to_rse-(\d+)\.csv',
        fr'{re.escape(folder_prefix)}devices_to_backend-(\d+)\.csv'
    ]

    # Extract numbers from filenames in the latest date folder
    matched_files = []
    extracted_numbers = []
    for obj in response.get('Contents', []):
        file_key = obj['Key']
        print(f"file_key: {file_key}")
        # Check against each pattern
        for pattern in patterns:
            match = re.search(pattern, file_key)
            if match:
                print(f"Match found with pattern '{pattern}': {match.group(0)}")
                number = int(match.group(1))
                extracted_numbers.append(number)
                matched_files.append(match.group(0))
                break
    
    print("Matched files:")
    for matched_file in matched_files:
        print(matched_file)
        # Check if 'backend_to_rse' is in the matched file key
        if 'backend_to_rse' in matched_file:
            # Perform the regex search within the matched_file
            match = re.search(r'backend_to_rse-(\d+)\.csv', matched_file)
            if match:
                number1 = int(match.group(1))
                print(f"Matched 'backend_to_rse' number: {number1}")
        elif 'backend_to_obd' in matched_file:
            # Perform the regex search within the matched_file for 'backend_to_obd'
            match = re.search(r'backend_to_obd-(\d+)\.csv', matched_file)
            if match:
                number2 = int(match.group(1))
                print(f"Matched 'backend_to_obd' number: {number2}")
        elif 'devices_to_backend' in matched_file:
            # Perform the regex search within the matched_file for 'devices_to_backend'
            match = re.search(r'devices_to_backend-(\d+)\.csv', matched_file)
            if match:
                number3 = int(match.group(1))
                print(f"Matched 'devices_to_backend' number: {number3}")
        else:
            print(f"No match found in '{matched_file}'")

    # Find the highest number in the latest date folder
    if extracted_numbers:
        print(f"Latest Date: {latest_date_str}, Latest Number: {extracted_numbers}, FILE_KEY: {file_key}")
    else:
        return {
            'statusCode': 404,
            'body': f"No files found in folder: {folder_prefix}"
        }
    

    # Email details
    SENDER = "test@example.com"
    RECIPIENT = "test@example.com"
    SUBJECT = f"AWS Lambda Test Email {todays_date}"
    BODY_TEXT = f"Amazon SES Test (Python)\r\nExtracted number: {extracted_numbers}"
    BODY_HTML = f"""<html>
    <head></head>
    <body>
      <h1>Amazon SES Test (Python)</h1>
      <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://boto3.amazonaws.com/v1/documentation/api/latest/index.html'>AWS SDK for Python (Boto)</a>.
      </p>
      <table border='1'>
        <tbody>
        <tr>
        <td width="287" colspan="2" valign="top" style="width:215.55pt;border:solid windowtext 1.0pt;background:#bfbfbf;padding:0in 5.4pt 0in 5.4pt">
        <p align="center" style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in;text-align:center">
        <b><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:black">Count of S Messages Processed</span></b></p>
        </td>
        </tr>
        <tr>
        <td width="198" valign="top" style="width:148.8pt;border:solid windowtext 1.0pt;border-top:none;background:#bfbfbf;padding:0in 5.4pt 0in 5.4pt">
        <p style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in">
        <b><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:black">Title</span></b></p>
        </td>
        <td width="89" valign="top" style="width:66.75pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;background:#bfbfbf;padding:0in 5.4pt 0in 5.4pt">
        <p align="center" style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in;text-align:center">
        <b><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:black">Total Count</span></b></p>
        </td>
        </tr>
        <tr>
        <td width="198" valign="top" style="width:148.8pt;border:solid windowtext 1.0pt;border-top:none;padding:0in 5.4pt 0in 5.4pt">
        <p style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in">
        <span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif">pps / devices_to_back</span></p>
        </td>
        <td width="89" valign="top" style="width:66.75pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
        <p align="center" style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in;text-align:center">
        <span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif">{number3}</span></p>
        </td>
        </tr>
        <tr>
        <td width="198" valign="top" style="width:148.8pt;border:solid windowtext 1.0pt;border-top:none;padding:0in 5.4pt 0in 5.4pt">
        <p style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in">
        <span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif">pps / back_to_o</span></p>
        </td>
        <td width="89" valign="top" style="width:66.75pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
        <p align="center" style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in;text-align:center">
        <span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif">{number2}</span></p>
        </td>
        </tr>
        <tr>
        <td width="198" valign="top" style="width:148.8pt;border:solid windowtext 1.0pt;border-top:none;padding:0in 5.4pt 0in 5.4pt">
        <p style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in">
        <span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif">pps / back_to_r</span></p>
        </td>
        <td width="89" valign="top" style="width:66.75pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
        <p align="center" style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in;text-align:center">
        <span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif">{number1}</span></p>
        </td>
        </tr>
        </tbody>
      </table>
      <br><br>
      <table border='1'>
        <tbody>
        <tr>
        <td width="318" colspan="2" valign="top" style="width:238.25pt;border:solid windowtext 1.0pt;background:#bfbfbf;padding:0in 5.4pt 0in 5.4pt;height:25.15pt">
        <p style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in;text-align:center"">
        <b><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:black">Count of S related Incident/Service Request</span></b></p>
        <p align="center" style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in;text-align:center">
        <b><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:black">&nbsp;</span></b></p>
        </td>
        </tr>
        <tr>
        <td width="198" valign="top" style="width:148.8pt;border:solid windowtext 1.0pt;border-top:none;background:#bfbfbf;padding:0in 5.4pt 0in 5.4pt">
        <p style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in">
        <b><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:black">Title</span></b></p>
        </td>
        <td width="119" valign="top" style="width:89.45pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;background:#bfbfbf;padding:0in 5.4pt 0in 5.4pt">
        <p align="center" style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in;text-align:center">
        <b><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:black">Total Count</span></b></p>
        </td>
        </tr>
        <tr>
        <td width="198" valign="top" style="width:148.8pt;border:solid windowtext 1.0pt;border-top:none;padding:0in 5.4pt 0in 5.4pt">
        <p style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in">
        <span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif">Incident Request</span></p>
        </td>
        <td width="119" valign="top" style="width:89.45pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
        <p align="center" style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in;text-align:center">
        <span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif">0</span></p>
        </td>
        </tr>
        <tr>
        <td width="198" valign="top" style="width:148.8pt;border:solid windowtext 1.0pt;border-top:none;padding:0in 5.4pt 0in 5.4pt">
        <p style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in">
        <span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif">Service Request</span></p>
        </td>
        <td width="119" valign="top" style="width:89.45pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
        <p align="center" style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in;text-align:center">
        <span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif">0</span></p>
        </td>
        </tr>
        </tbody>
      </table>
    </body>
    </html>
                """

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name='us-east-1')

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': e.response['Error']['Message']
        }
    else:
        return {
            'statusCode': 200,
            'body': "Email sent! Message ID: {}".format(response['MessageId'])
        }
