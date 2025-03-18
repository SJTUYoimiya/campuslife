import argparse
from scripts.data_handler import Config
from scripts.network.user_service import AccountService
from scripts.network.charge_service import Charge


def login():
    AccountService()

def charge_status():
    user_info = Config('user_info').value
    user_id = user_info['userid']
    Charge(user_id).charge_status

def charge():
    user_info = Config('user_info').value
    user_id = user_info['userid']

    charge_handler = Charge(user_id)

    if not charge_handler.charge_status:
        charger_serial = input('Enter the serial number of the charger: ')
        _ = charge_handler.charge(charger_serial)

def main():
    parser = argparse.ArgumentParser(description='Select a function')
    parser.add_argument('func', type=str, help='The function to run')
    args = parser.parse_args()

    if args.func == 'login':
        login()
    elif args.func == 'charge':
        charge()
    elif args.func == 'status':
        charge_status()
    else:
        exit(1)

if __name__ == "__main__":
    main()
