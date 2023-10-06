import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import random

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False, slow_mo= 50)
#     page = browser.new_page()
#     page.goto("https://cas.ucalgary.ca/cas/login?service=https%3a%2f%2fd2l.ucalgary.ca%2fd2l%2fcustom%2fcas&ca.ucalgary.authent.ucid=true")
    
#     #Inputs into all of these function that take two arguments are first is css selector and if their is a second arugment it is an input that we are passing back
#     page.fill("input#eidtext",'drew.vandenbosch')
#     page.fill("input#passwordtext","Bomber4444")
#     page.click('input#signinbutton')
#     # page.is_visible('')
#     html = page.inner_html('body > div.d2l-page-main.d2l-max-width.d2l-min-width > div.d2l-page-main-padding > div.d2l-homepage')
    
#     #printing out the conent of the main page
#     # print(html)
    
#     #now parsing the data with boutiful soup -> learn more about beaurtiful soup and playwright
#     soup = BeautifulSoup(html,'html.parser')
#     print(soup.find_all('class'))
    
birthdays = {'Alice': 'Apr 1', 'Bob': 'Dec 12', 'Carol': 'Mar 4'}

while True:
    print('Enter a name: (blank to quit)')
    name = input()
    if name == '':
        break
    
if name in birthdays:
        print(birthdays[name] + ' is the birthday of ' + name)
else:
        print('I do not have birthday information for ' + name)
        print('What is their birthday?')
        bday = input()
        birthdays[name] = bday
        print('Birthday database updated.')

    
    


