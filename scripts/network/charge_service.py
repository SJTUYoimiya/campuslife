"""
This module provides the Charge class to interact with the charge service.
"""
from .user_service import post

url = "http://kld.sjtu.edu.cn/campuslifedispatch/WebService.asmx/ChargeService"

def get_charger_list(rid: str | int = None) -> dict:
    """
    Get the list of chargers.

    Parameters
    ----------
    rid : str | int, optional
        The id of the charger, by default None
        if rid is not provided, return the list of all chargers
        if rid is provided, return the list of sub-chargers

    Returns
    -------
    dict
        The list of chargers
    """
    order_data = {"ordertype": "getsublist", "rid": str(rid)} if rid else {"ordertype": "getlist"}
    return post(url, order_data)
    
class Charge:
    """
    A class to interact with the charge service.

    Attributes
    ----------
    user_id : str
        The user id
    charge_status : dict | None
        The charge status
    
    Methods
    -------
    charge(charger_serial: str)
        Charge at the charger with the given serial number
    """
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.get_charge_status()

    def get_charge_status(self) -> dict | None:
        order_data = {
            "userid": self.user_id,
            "ordertype": "chargestatus"
        }
        res_data = post(url, order_data)['result1']
        if res_data:
            self.charge_status = res_data[0]
            print(f"You are charging now at {self.charge_status['position']} since {self.charge_status['bgtime']}")
            print(f"Duration: {self.charge_status['duration']}, Amount: ¥{self.charge_status['amount']}")
        else:
            print('You are not charging now')
            self.charge_status = None

    def get_balance(self) -> None:
        order_data = {
            "userid": self.user_id,
            "ordertype": "priceinfo"
        }
        res_data = post(url, order_data)
        balance = res_data['result1'][0]
        if float(balance['allmoney']) >= float(balance['leftmoney']):
            raise Exception("You don't have enough balance")

    def charge(self, charger_serial: str) -> dict:
        """
        Charge at the charger with the given serial number.

        First, check if the user is charging now.
        Then, get the balance of the user.
        Finally, if both checks pass, send the charge request to the charge server.
        """
        if self.charge_status:
            exit(0)

        self.get_balance()

        if not charger_serial.isdigit():
            raise TypeError('Charger serial must be digits')
        elif len(charger_serial) != 8 and len(charger_serial) != 16:
            raise ValueError('Charger serial must be 8 or 16 digits')

        order_data = {
            "userid": self.user_id,
            "ordertype": "docharge",
            "qrcode": charger_serial
        }
        return post(url, order_data)