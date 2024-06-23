import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "test@example.com"

    # Replace recipient@example.com with a "To" address.
    # If your account is still in the sandbox, this address must be verified.
    RECIPIENT = "test@example.com"

    # The subject line for the email.
    SUBJECT = "AWS Lambda Test Email with Two Tables"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                )

    # The HTML body of the email with two tables.
    BODY_HTML = """<html>
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
        <span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif">tps / devices_to_back</span></p>
        </td>
        <td width="89" valign="top" style="width:66.75pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
        <p align="center" style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in;text-align:center">
        <span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif">9</span></p>
        </td>
        </tr>
        <tr>
        <td width="198" valign="top" style="width:148.8pt;border:solid windowtext 1.0pt;border-top:none;padding:0in 5.4pt 0in 5.4pt">
        <p style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in">
        <span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif">tps / back_to_o</span></p>
        </td>
        <td width="89" valign="top" style="width:66.75pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
        <p align="center" style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in;text-align:center">
        <span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif">1</span></p>
        </td>
        </tr>
        <tr>
        <td width="198" valign="top" style="width:148.8pt;border:solid windowtext 1.0pt;border-top:none;padding:0in 5.4pt 0in 5.4pt">
        <p style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in">
        <span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif">tps / back_to_r</span></p>
        </td>
        <td width="89" valign="top" style="width:66.75pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
        <p align="center" style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in;text-align:center">
        0</p>
        </td>
        </tr>
        </tbody>
      </table>
      <br><br>
      <table border='1'>
        <tbody>
        <tr>
        <td width="318" colspan="2" valign="top" style="width:238.25pt;border:solid windowtext 1.0pt;background:#bfbfbf;padding:0in 5.4pt 0in 5.4pt;height:25.15pt">
        <p style="margin-right:0in;margin-left:0in;font-size:12pt;font-family:Aptos,sans-serif;margin:0in">
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
