# -*- coding: utf-8 -*-
#This algorith takes product name, price and discount from the given n11.com url for every page
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

start_url = 'https://www.n11.com/bilgisayar/bilgisayar-bilesenleri/hard-disk'
#start url

sort_mod = 'PRICE_LOW'
#sort mod (PRICE_LOW, PRICE_HIGH, SALES_VOLUME, REVIEWS, NEWEST, REVIEW_RATE, SELLER_GRADE)

sfilter = 'ssd'
#if you need you can define a filter

kapasite = '480%20GB'
#this filter is just for ssd
addCount = 0

#applying url adds
if sort_mod != "":
    if addCount == 0:
        start_url += "?"
        
    start_url += "srt=" + sort_mod + "&"
    addCount+=1
    
if sfilter != "":
    if addCount == 0:
        start_url += "?"
    start_url += "iw=" + sfilter + "&"
    addCount+=1

if kapasite != "":
    if addCount == 0:
        start_url += "?"
    start_url += "kapasite=" + kapasite
    addCount+=1
    
now = datetime.now()
dt_string = now.strftime("%d.%m.%Y %H.%M.%S")
#taking date for file name

with open(dt_string + ".csv", 'a+', encoding = 'utf-8') as f:
    #creating file
    f.write("Name;Price(TL);Discount Ratio(%);URL\n")
    #writing csv header
    while True:
        r = requests.get(start_url)
        #taking site
        source = BeautifulSoup(r.content,"lxml")        
        products = source.find_all("li", attrs = {"class":"column"})
        #finding all products on the page
                
        for product in products:
            #getting product name, price and discount
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
                #deleting ad products
                continue
            
            
            print(product_name)
            print(price)
            print("Discount Ratio: %", discount_raito)
            print(url['href'])
            #writing product values to file 
            line = product_name + ";" + price + ";" + discount_raito + ";" + url['href'] + "\n"
            
            f.write(line)
       #taking new page's url
        try:
            start_url = source.find("a", attrs = {"class":"next navigation"})["href"]
        except:
            break
