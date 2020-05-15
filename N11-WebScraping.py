# -*- coding: utf-8 -*-
"""
Created on Wed May 13 16:31:40 2020
N11 Sitesinden ürün fiyatlarını çekme algoritması
@author: ertug
"""
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

start_url = 'https://www.n11.com/bilgisayar/bilgisayar-bilesenleri/hard-disk'
sort_mod = 'PRICE_LOW'
sfilter = 'ssd'
kapasite = '480%20GB'

if sort_mod != "":
    start_url += "?srt=" + sort_mod + "&"
    
if sfilter != "":
    start_url += "iw=" + sfilter + "&"
    
if kapasite != "":
    start_url += "kapasite=" + kapasite

now = datetime.now()
dt_string = now.strftime("%d.%m.%Y %H.%M.%S")

with open(dt_string + ".csv", 'a+', encoding = 'utf-8') as f:
    f.write("Name;Price(TL);Discount Ratio(%);URL\n")
    while True:
        r = requests.get(start_url)

        source = BeautifulSoup(r.content,"lxml")
        products = source.find_all("li", attrs = {"class":"column"})
        
        try:
            start_url = source.find("a", attrs = {"class":"next navigation"})["href"]
        except:
            break
        
        
        for product in products:
            
            product_name = product.find("h3", attrs = {"class":"productName"}).text
            product_name = re.sub(' +', ' ', product_name)
            product_name = str.replace(product_name, '\n', '')
            
            price = product.find("ins").text
            price = re.sub("[^0-9,.]", "", price)
            
            discount_raito = ""
            
            try:
                discount_raito = product.find("span", attrs = {"class": "ratio"}).text
                discount_raito = str.replace(discount_raito, " ", "")
            except AttributeError:
                discount_raito = "0"
                
            
            url = product.find("a", attrs = {"class":"plink"})
            
            if url['href'][-12:] == "one-cikanlar":
                continue
            
            print(product_name)
            print(price)
            print("Discount Ratio: %", discount_raito)
            print(url['href'])
            line = product_name + ";" + price + ";" + discount_raito + ";" + url['href'] + "\n"
            
            f.write(line)
            
        
        