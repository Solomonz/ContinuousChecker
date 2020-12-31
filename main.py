#! /usr/bin/env python3

from datetime import datetime
from sys import argv, exit
from time import sleep
from json import load
from notify import notify


## Import Site-Specific Checkers


CHECK = {
        }


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if __name__ == "__main__":
    with open('catalog.json') as catalog_file:
        catalog = load(catalog_file)

    while True:
        for item in catalog:
            print(f"{bcolors.HEADER}{str(datetime.now())}{bcolors.ENDC}  ||  {bcolors.OKBLUE}[[ {item['website']} ]]{bcolors.ENDC}  {bcolors.BOLD}{item['name']}{bcolors.ENDC}  ::  ", end="")
            try:
                if CHECK[item['website']](item):
                    print(f"{bcolors.OKCYAN}available! notifying now{bcolors.ENDC}")
                    notify(item['name'], item['website'], item['url'])
                else:
                    print(f"{bcolors.FAIL}not available{bcolors.ENDC}")
            except Exception:
                print(f"{bcolors.WARNING}CAPTCHA{bcolors.ENDC}")

        sleep(10)
