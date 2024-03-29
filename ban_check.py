import os
import http.client
import json
import sys
import time
from datetime import datetime
import inquirer

accounts = list()

account_dir = "accounts"

for file in os.listdir(account_dir):
    if file.endswith(".txt"):
        accounts.append(file.replace('.txt', ''))

account_selection = [
    inquirer.List('username',
                  message="Please select which account you want to check",
                  choices=accounts,
                  ),
]

refresh = [
    inquirer.Text('refresh',
                  message="Set interval in seconds",
                  default=60
                  ),
]

count = [
    inquirer.Text('count',
                  message="How many times do you want this script to check the appeal page?",
                  default=20
                  ),
]

prepare_account_username = inquirer.prompt(account_selection)
prepare_refresh = inquirer.prompt(refresh)
prepare_count = inquirer.prompt(count)

username = str(prepare_account_username['username'])
refresh = int(prepare_refresh['refresh'])
count = int(prepare_count['count'])

cookie = open(os.path.join(account_dir, username + '.txt'), 'r').read()


class ConsoleColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def account():
    return []


def currenttime():
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def console(message, style='default'):
    if style == "default":
        print(f"[{ConsoleColor.OKGREEN}{currenttime()}{ConsoleColor.ENDC}]: {message}")
    elif style == "warning":
        print(
            f"[{ConsoleColor.OKGREEN}{currenttime()}{ConsoleColor.ENDC}]: {ConsoleColor.WARNING}{message}{ConsoleColor.ENDC}")
    elif style == "danger":
        print(
            f"[{ConsoleColor.OKGREEN}{currenttime()}{ConsoleColor.ENDC}]: {ConsoleColor.FAIL}{message}{ConsoleColor.ENDC}")
    elif style == "info":
        print(
            f"[{ConsoleColor.OKGREEN}{currenttime()}{ConsoleColor.ENDC}]: {ConsoleColor.OKCYAN}{message}{ConsoleColor.ENDC}")
    elif style == "success":
        print(
            f"[{ConsoleColor.OKGREEN}{currenttime()}{ConsoleColor.ENDC}]: {ConsoleColor.OKGREEN}{message}{ConsoleColor.ENDC}")


def contact_activision(endpoint):
    conn = http.client.HTTPSConnection("support.activision.com")
    payload = ''
    headers = {
        'X-Activision-Countrycode': 'US',
        'Cookie': cookie,
        # 'Authorization': 'Bearer ' + bearer
    }
    conn.request("GET", endpoint, payload, headers)
    res = conn.getresponse()

    if res.status != 200:
        console("Unable to retrieve account data! Please check your credentials", 'warning')
        exit()

    return json.loads(res.read().decode("utf-8"))


def accountinfo():
    console("Connecting to support.activision.com, one moment please.")
    accountdata = contact_activision('/api/profile?accts=false')
    console(
        f"Success! Account: {accountdata['username']} Email: {accountdata['email']} Created: {accountdata['created']}")


def checkapeal(ban):
    if ban['canAppeal']:
        console("This ban can be appealed!", 'info')
    else:
        console("This ban cannot be appealed anymore!", 'danger')


def exit_script(message):
    console(f"Shutting down script! {message}", "info")
    exit()


def docheck():
    shutdown = False
    shutdownmsg = ''
    console("Fetching data from Activision...")
    accountdata = contact_activision("/api/bans/appeal?locale=en")

    if accountdata['success']:
        if len(accountdata['bans']) == 0:
            console("No ban detected for this account!", 'success')
        else:
            for ban in accountdata['bans']:
                if ban['enforcement'] == 'PERMANENT':
                    console(f"Perm ban detected for {ban['title']}", 'danger')
                    checkapeal(ban)

                    shutdown = True
                    shutdownmsg = "No need to check anymore as the account is permanently banned"
                else:
                    console(f"This account is shadow banned/in limited matchmaking for {ban['title']}", 'danger')
                    checkapeal(ban)

    else:
        console(f"Request returned the following error: {accountdata['error']}", 'warning')

    if shutdown:
        exit_script(shutdownmsg)


def delay_indicator():
    prefix = f"[{ConsoleColor.OKGREEN}{currenttime()}{ConsoleColor.ENDC}]: "
    for remaining in range(refresh, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write(prefix + "Check complete! Checking again in {:2d} seconds.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write('\n')


accountinfo()

i = 1
while i < count:
    docheck()
    delay_indicator()
    i += 1
