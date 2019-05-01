"""***************************************************************
**  Program Name:   BookDepository				**
**  Version Number: V0.9                                        **
**  Copyright (C):  February 16, 2017 Richard W. Allen          **
**  Date Started:   October 1, 2016                             **
**  Date Ended:     February 16, 2017                           **
**  Author:         Richardn W. Allen                           **
**  Webpage:        http://www.richardallenonline.com/          **
**  IDE:            IDLE 2.7.11                                 **
**  Compiler:       Python 2.7.11                               **
**  Langage:        Python 2.7.11				**
**  License:	    GNU GENERAL PUBLIC LICENSE Version 2	**
**		    see license.txt for for details	        **
***************************************************************"""
#!/usr/bin/python
import database
from database import ItemsDataset
from database import UnavailableDataset

import time
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from lxml import html
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read("creds")
email_user = config.get('email','user')
email_pass = config.get('email','pass')


# Change these values to your desired sale page.
BASE_URL = "http://www.bookdepository.com/Star-Wars-X-Wing-Fantasy-Flight-Games/"
SMTP_URL = "smtp.gmail.com:587"
#XPATH_SELECTOR = '//*[@class="price"]'
XPATH_SELECTOR = '//*[@class="sale-price"]'
XPATH_SELECTOR2 = '//*[@class="red-text bold"]'
#XPATH_SELECTOR = '//*[@id="priceblock_ourprice"]'
SLEEP_INTERVAL = 3600
#ITEMS is a list of lists, storing ASINs and their maximum prices
ITEMS = [['9781616613778',14,'X-Wing'],
         ['9781616616779',14,'Tie Bomber'],
         ['9781616613785',14,'Tie Fighter'],
         ['9781616619398',14,'M3-A'],
         ['9781616617745',14,'Tie Phantom'],
         ['9781616617738',14,'E-Wing'],
         ['9781616617714',14,'Z-95'],
         ['9781616619381',14,'Starviper'],
         ['9781616613808',14,'Tie Advanced'],
         ['9781616616762',14,'B-Wing'],
         ['9781616617721',14,'Tie Defender'],
         ['9781616617042',14,'Hwk-290'],
         ['9781616615383',14,'Tie Interceptor'],
         ['9781616615376',14,'A-Wing'],
         ['9781616613792',14,'Y-Wing'],
         ['9781616619404',25,'IG-2000'],
         ['9781616616755',25,'Lambda-Class Shuttle'],
         ['9781616618032',25,'Imperial Aces'],
         ['9781616615352',25,'Millennium Falcon'],
         ['9781616619176',25,'YT-2400'],
         ['9781616619183',25,'VT-49'],
         ['9781616616748',45,'Rebel Transport'],
         ['9781633441446',60,'Imperial Assault Carrier'],
         ['9781616617691',80,'Tantive IV'],
         ['9781616615369',25,'Slave I'],
         ['9781616619114',25,'Rebel Aces'],
         ['9781616619411',40,'Most Wanted'],
         ['9781616619671',80,'Imperial Raider'],
         ['9781633440715',14,'K-Wing'],
         ['9781633440722',14,'Tie Punisher'],
         ['9781616610395',20,'Cosmic Conflict'],
         ['9781616613624',20,'Cosmic Alliance'],
         ['9781616616519',20,'Cosmic Storm'],
         ['9781616619138',20,'Cosmic Dominion']
	]
#ITEMS = [['B0042A8CW2',100]]
PERSENT = [50, 30]

db = database.Database()

def send_email(price, url, name, backinstock = False):
    global BASE_URL

    try:
        s = smtplib.SMTP(SMTP_URL)
        s.ehlo()
        s.starttls()
        s.login(email_user, email_pass)
    except smtplib.SMTPAuthenticationError:
        print("Failed to login")
    else:
        print("Logged in! Composing message..")
        msg = MIMEMultipart("alternative")
        if backinstock == True:
            msg["Subject"] = "Back in stock Alert - {}".format(price)
        else:
            msg["Subject"] = "Price Alert - {}".format(price)
        msg["From"] = email_user
        msg["To"] = email_user
        text = "{2} The price is currently {0} !! URL to salepage: {1}".format(price, BASE_URL, name) + url
        part = MIMEText(text, "plain")
        msg.attach(part)
        s.sendmail(email_user, email_user, msg.as_string())
        s.quit()
        print("Message has been sent.")
        
def main():
    while True:
        #item[0] is the item's ASIN while item[1] is that item's maximum price
        for item in ITEMS:
            try:
                r = requests.get(BASE_URL + item[0])
                tree = html.fromstring(r.text)
            except:
                print("Error!")
            try:
                txt = tree.xpath(XPATH_SELECTOR2)[0].text.strip()
                print txt + " " + item[2]
                if txt == "Currently unavailable":
                   db.AddUnavailable(UnavailableDataset(int(item[0])))
                            
            except IndexError:
                try:
                    #We have to strip the dollar sign off of the number to cast it to a float
                    #print len(tree.xpath(XPATH_SELECTOR)[0].text[1:])
                    txt = tree.xpath(XPATH_SELECTOR)[0].text.strip()
                    price = float(txt[2:])
                except IndexError:
                    print("Didn't find the 'price' element, trying again")
                    continue
                if db.RemoveUnavailable(UnavailableDataset(int(item[0]))) == True:
                    print("Back in stack {} is {}!!".format(item[2], price))
                    send_email(price, item[0], item[2], True)
                    
                if db.AddItem(ItemsDataset(0,int(item[0]), price)) == True:
                    
                        
                    print("New low price for {} is {}!!".format(item[2], price))
                    """if price <= item[1]:
                    print("Price is {}!! Trying to send email.".format(price) + " " + item[2])"""
                    send_email(price, item[0], item[2])
                    #break
                else:
                    print("Price is {}. Ignoring...".format(price) + " " + item[2])
    
        print "Sleeping for {} seconds".format(SLEEP_INTERVAL)
        time.sleep(SLEEP_INTERVAL)
    
if __name__ == "__main__":
    main()
    del db
