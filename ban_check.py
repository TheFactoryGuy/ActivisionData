import os
import http.client
import json
import sys
import time
from datetime import datetime
import inquirer

# Constants
ACCOUNT_DIR = "accounts"
DEFAULT_REFRESH_INTERVAL = 60
DEFAULT_CHECK_COUNT = 20


# Function to load account names from files
def load_accounts(directory):
    accounts = []
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            accounts.append(file.replace('.txt', ''))
    return accounts


# Function to retrieve cookie from file
def load_cookie(username, directory):
    filename = os.path.join(directory, username + '.txt')
    with open(filename, 'r') as file:
        return file.read().strip()


# Function to display colored messages in console
def console(message, style='default'):
    colors = {
        "default": "",
        "warning": "\033[93m",
        "danger": "\033[91m",
        "info": "\033[96m",
        "success": "\033[92m"
    }
    print(f"[{datetime.now().strftime('%H:%M:%S')}]: {colors.get(style, '')}{message}\033[0m")


# Function to fetch data from Activision API
def contact_activision(endpoint, cookie):
    conn = http.client.HTTPSConnection("support.activision.com")
    headers = {
        'X-Activision-Countrycode': 'US',
        'Cookie': cookie,
    }
    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    if res.status != 200:
        console("Unable to retrieve account data! Please check your credentials", 'warning')
        sys.exit()
    return json.loads(res.read().decode("utf-8"))


# Function to check if an account has an appeal able ban
def check_appeal(ban):
    if ban['canAppeal']:
        console("This ban can be appealed!", 'info')
    else:
        console("This ban cannot be appealed anymore!", 'danger')


# Function to exit the script with a message
def exit_script(message):
    console(f"Shutting down script! {message}", "info")
    sys.exit()


# Function to perform initial account info check
def account_info(cookie):
    console("Connecting to support.activision.com, one moment please.")
    account_data = contact_activision('/api/profile?accts=false', cookie)
    console(
        f"Success! Account: {account_data['username']} Email: {account_data['email']} Created: {account_data['created']}")


# Function to perform the ban check
def do_check(cookie):
    console("Fetching data from Activision...")
    ban_data = contact_activision("/api/bans/appeal?locale=en", cookie)

    if ban_data['success']:
        if len(ban_data['bans']) == 0:
            console("No ban detected for this account!", 'success')
        else:
            for ban in ban_data['bans']:
                if ban['enforcement'] == 'PERMANENT':
                    console(f"Perm ban detected for {ban['title']}", 'danger')
                    check_appeal(ban)
                    exit_script("No need to check anymore as the account is permanently banned")
                else:
                    console(f"This account is shadow banned/in limited matchmaking for {ban['title']}", 'danger')
                    check_appeal(ban)
    else:
        console(f"Request returned the following error: {ban_data['error']}", 'warning')


# Function to display delay indicator
def delay_indicator(refresh):
    for remaining in range(refresh, 0, -1):
        sys.stdout.write(
            f"\r[{datetime.now().strftime('%H:%M:%S')}]: Check complete! Checking again in {remaining} seconds.")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write('\n')


# Main function
def main():
    accounts = load_accounts(ACCOUNT_DIR)
    if not accounts:
        sys.exit('No accounts found!')

    account_selection = inquirer.prompt([
        inquirer.List('username',
                      message="Please select which account you want to check",
                      choices=accounts)
    ])
    username = account_selection['username']
    cookie = load_cookie(username, ACCOUNT_DIR)

    account_info(cookie)

    refresh = inquirer.prompt([
        inquirer.Text('refresh',
                      message="Set interval in seconds",
                      default=DEFAULT_REFRESH_INTERVAL)
    ])['refresh']
    refresh = int(refresh)

    count = inquirer.prompt([
        inquirer.Text('count',
                      message="How many times do you want this script to check the appeal page?",
                      default=DEFAULT_CHECK_COUNT)
    ])['count']
    count = int(count)

    for i in range(count):
        do_check(cookie)
        delay_indicator(refresh)


if __name__ == "__main__":
    main()
