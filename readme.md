# ActivisionDataChecker/Activison API tool

This tool will let you access the Activision API to get your account information! 

## DISCLAIMER
This code is provided solely for educational purposes. It is intended to serve as a learning tool and to demonstrate programming concepts. The code may not be suitable for production environments and should not be used for any commercial or operational purposes.

While efforts have been made to ensure the accuracy and reliability of the code, no guarantee is made regarding its correctness or completeness. Users are encouraged to review and modify the code according to their own requirements and best practices.

**Please note that the author is not a professional Python developer and acknowledges that the code can always be improved. This code was created as a means to test and enhance Python programming skills.**

Under no circumstances shall the authors or distributors of this code be liable for any damages, losses, or legal issues arising from its use. Use of this code is at the sole risk of the user.

By using this code, you agree to waive any claims or liabilities against the authors or distributors for any consequences resulting from its use.

## Requirements
1. inquirer -> pip install inquirer or pip3 install inquirer

## Getting started!
1. Create a folder named accounts.
2. For each account create a text file. For example; mytestaccount.txt
3. Go to "https://support.activision.com/ban-appeal" and login to your account. Once logged in open the browser inspection and go to the network tab. There will be a request to your profile that's looks like this "profile?accts=false". Click on this request and in the request headers sections you will find a param called "cookie". Copy the contents of the cookie params and save this to your account .txt file.

## Currently available tools;

1. Ban appeal check

   The tool (ban_check.py) will check the appeal page if your account is banned or in limited matchmaking and will check in intervals provided by the user input.
