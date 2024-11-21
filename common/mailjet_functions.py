from mailjet_rest import Client
import os
api_key = os.environ['MJ_APIKEY_PUBLIC']
api_secret = os.environ['MJ_APIKEY_PRIVATE']
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

def send_email(email, name, subject, text, html):
    data = {
        'Messages': [
                    {
                            "From": {''
                                    "Email": 'betweenjobsplatform@gmail.com',
                                    "Name": "BetweenJobs"
                            },
                            "To": [
                                    {
                                            "Email": email,
                                            "Name": name
                                    }
                            ],
                            "Subject": subject,
                            "TextPart": text,
                            "HTMLPart": html,
                    }
            ]
        }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())