"""
This script is used to send messages to iPhone using Bark.app.
For more information, please visit https://bark.day.app/.

Usage:
    1. Download the Bark app from App Store on iPhone.
    2. Open the app and get the device key.
    3. Save the device key to configs.json like this:
        {"bark": {"device_key": "YOUR_DEVICE_KEY"}}
    4. Run this script to send messages to your iPhone.
"""
import requests

baseURL = "https://api.day.app/push"
headers = {'Content-Type': 'application/json; charset=utf-8'}

def bark(messages: list[dict[str, str]], device_key: str):
    for message in messages:
        data = {
            'device_key': device_key,
            'title': message['msgtitle'],
            'subtitle': message['msgtime'],
            'body': message['msgcontent'],
            'group': 'CampusLife',
            'isArchive': 1,
            'icon': 'https://sjtuyoimiya.github.io/images/campuslife.png'
        }
        requests.post(baseURL, headers=headers, json=data)

def bark_wrapper(messages: list[dict[str, str]]):
    from ..data_handler import Config
    device_key = Config('bark').value.get('device_key')
    bark(messages, device_key)
