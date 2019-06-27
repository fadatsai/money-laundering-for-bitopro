#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json,time,sys
import base64, hmac, hashlib
import requests

def public(url):
    baseUrl = "https://api.bitopro.com/v2"
    completeURL = baseUrl + url
    response = requests.get(completeURL)
    data=response.json()
    return data
    
def order(action,amount,price):
    baseUrl = "https://api.bitopro.com/v2"
    url="/orders/"+ PAIR
    nonce = int(time.time() * 1000)
    completeURL = baseUrl + url
    body = {
        'action': action,
        'amount': str(amount),
        'price': str(price),
        'timestamp': nonce,
        'type': 'limit'
    }
    payload = base64.urlsafe_b64encode(json.dumps(body).encode('utf-8')).decode('utf-8')
    signature = hmac.new(API_SECRET, payload, hashlib.sha384).hexdigest()
    headers = {
        'X-BITOPRO-APIKEY': API_KEY,
        'X-BITOPRO-PAYLOAD': payload,
        'X-BITOPRO-SIGNATURE': signature,
    }
    response = requests.post(completeURL, headers=headers, json=body)
 
        
if __name__ == '__main__':
    
    ###########################################################################
    API_KEY = ""
    API_SECRET = ""
    PAIR = "btc_twd"
    AMOUNT = float(0.1)
    TARGER_VOLUME = 10000000
    ###########################################################################    
    order_book = public("/order-book/"+ PAIR)
    current_ask_price = order_book['asks'][0]['price']
    current_bid_price = order_book['bids'][0]['price']
    ticker = public("/ticker/" + PAIR)
    last_price = ticker['lastPrice']
    print "-----------------------------------------"
    print "Current ask Price: " + current_ask_price
    print "Current bid Price: " + current_bid_price
    print "Lart Price: " + last_price
    print "-----------------------------------------"
    count = int(round(TARGER_VOLUME / (AMOUNT * float(last_price))) / 2)
    for i in range(count):
        print i
        order_book = public("/order-book/" + PAIR )
        current_ask_price = order_book['asks'][0]['price']
        current_bid_price = order_book['bids'][0]['price']
        price = int(int(current_ask_price)-1)
        print price
        if price == int(current_ask_price) or price == int(current_bid_price):
            print "Pirce too close"
            sys.exit(1) 
        order("sell",AMOUNT,price)
        order("buy",AMOUNT,price)
