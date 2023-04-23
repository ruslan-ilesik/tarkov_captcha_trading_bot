# importing modules
import configparser

settings = configparser.ConfigParser()
settings.read('./settings.ini')

import pyautogui
screen = pyautogui.size()
import my_sleep as time
import find_price
import json
from tqdm import tqdm
from constants import *
import search
import buy
import change_tabs
import sale
import time as realtime
import get_image_by_name

print("Loading items...")
file = open("./config.json",'r', encoding="utf8")
list = json.loads(file.read())
for i in tqdm(list):
    if not "currency" in i.keys():
        i["currency"] = "RUB"
    if not "currency_buy" in i.keys():
        i["currency_buy"] = i["currency"]
    if not "currency_sell" in i.keys():
        i["currency_sell"] = i["currency_buy"]
file.close()
print("Starting...")
print("You have 5 seconds")
for i in tqdm(range(50)):
    realtime.sleep(0.1)
print("-"*30)
while 1:
    for i in list:
        search.clear()
        search.put_text(i["name"])
        search.select_first()
        price, img = find_price.get_smallest_price()
        p_like_buy = find_price.convert_to_rubles(price,find_price.get_currency(img))
        p_sell_rub = find_price.convert_to_rubles(i['price'],i["currency_sell"])
        buy_currency = find_price.get_currency(img)
        print("Checking object: ",i["name"])

        print("Found price: ",price, find_price.get_currency(img),
                ("( " + str(p_like_buy)+" RUB )" if buy_currency != "RUB" else ""))
        
        print("Sale price:",i['price'],i["currency_sell"],
                ("( "+str(p_sell_rub)+" RUB )"if i["currency_sell"] != "RUB" else ""))
        
        if (settings.getboolean("GLOBAL_SETTINGS","use_different_currencies") or find_price.is_currency(img,i["currency_buy"])):
            if p_like_buy < p_sell_rub and  p_sell_rub*2 > p_like_buy :
                buy.buy_first() 
                print("BUYING!, we can earn: ",
                        p_sell_rub-p_like_buy/settings.getint("CURRENCY",i["currency_sell"]),
                        i["currency_sell"],
                        ("( "+str(p_sell_rub-p_like_buy) +" RUB )" if i["currency_sell"] != "RUB" else ""))
                change_tabs.go_to_trader(i["trader"])
                sale.make_sale()
                change_tabs.change_to("FLEA_MARKET")
            else:
                print("Do not buy, price to high")
        else:
            print("Do not buy, price not in currency we are looking for")
        print("-"*30)
