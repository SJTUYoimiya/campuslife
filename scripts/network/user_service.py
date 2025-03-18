"""
This module provides functions to request user service from Campuslife app.
"""
import json
import requests
from bs4 import BeautifulSoup
from ..des import encrypt, decrypt
from ..data_handler import Config, save_data
from .bark_api import bark_wrapper

def post(url: str, order_data: dict[str, str]) -> dict[str, str]:
    """
    Post order data to the given url and return the response data.

    Parameters
    ----------
    url : str
        The url to post the order data.
    order_data : dict[str, str]
        The order data to post.

    Returns
    -------
    dict[str, str]
        The response data.
    """
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    res = requests.post(url, data=encrypt(order_data), headers=headers)
    res.raise_for_status()

    try:
        soup = BeautifulSoup(res.text, 'xml')
        string = soup.string.text
        res_data = decrypt(string)
        res_data = json.loads(res_data)
    except Exception as e:
        res_data = {"state": 0, "note": str(e)}

    if int(res_data.get('state', 0)) == 1:
        print(res_data.get('note', ''))
        return res_data['data']
    else:
        raise ValueError(res_data.get('note', 'Unknown error'))

def login(phone: str, password: str):
    """
    Login to Campuslife app with phone number and password.
    
    Parameters
    ----------
    phone : str
        The user's phone number.
    password : str
        The user's password.

    Returns
    -------
    dict[str, str]
        The user's information.
    """
    url = "http://kld.sjtu.edu.cn/campuslife/WebService.asmx/UserService"
    order_data = {
        "phone": phone,
        "logpass": password,
        "ordertype": "login"
    }
    return post(url, order_data)['result1'][0]

class AccountService:
    url = "http://kld.sjtu.edu.cn/campuslifedispatch/WebService.asmx/UserService"

    def __init__(self, user_info: dict[str, str] = None, path: str = 'configs.json'):
        if user_info:
            self.user_info = user_info
        elif path:
            self.load_user_info(path)
        else:
            raise ValueError("No user info provided.")

        account_info = self.get_account_info(
            self.user_info['userid'],
            self.user_info['acid']
        )

        self.user_info.update(account_info['result1'][0])
        self.user_info['feature'] = account_info['result2']
        Config('user_info', self.user_info, path=path).save()

    def load_user_info(self, path: str):
        try:
            self.user_info = Config('user_info', path=path).value
        except KeyError:
            pass
            
        try:
            login_info = Config('login_info', path=path).value
            phone = login_info['phone']
            password = login_info['password']
        except KeyError:
            print("No login info provided. Please login first.")
            phone = input("Phone: ")
            password = input("Password: ")
            cond = input("Save your phone & password? ([y]/n) ").strip().lower() or 'y'
            if cond == 'y':
                login_info = {"phone": phone, "password": password}
                Config('login_info', login_info, path=path).save()
            
        self.user_info = login(phone, password)
        Config('user_info', self.user_info, path=path).save()
    
    def get_account_info(self, user_id, acid):
        order_data = {
            "userid": user_id,
            "acid": acid,
            "ordertype": "accountinfo",
            "origin": "cloud"
        }
        return post(self.url, order_data)
    
    def get_message(self):
        order_data = {
            "username": self.user_info['username'],
            "phone": self.user_info['phone'],
            "userid": self.user_info['userid'],
            "ordertype": "getmessage",
            "acid": "0",
            "origin": "cloud"
        }

        res_data = post(self.url, order_data)
        max_message_id = res_data['result1'][0]['maxmsgid']
        if max_message_id:
            self.send_message(max_message_id)
            messages = res_data['result2']
            bark_wrapper(messages)
            save_data(messages, 'messages.json')
            print(messages)
        else:
            print("No new message.")
            return None
    
    def send_message(self, max_message_id):
        order_data = {
            "phone": self.user_info['phone'],
            "userid": self.user_info['userid'],
            "username": self.user_info['username'],
            "ordertype": "setmaxmsgid",
            "maxmsgid": str(max_message_id),
            "acid": self.user_info['acid'],
            "origin": "cloud",
        }

        _ = post(self.url, order_data)

if __name__ == "__main__":
    AccountService()