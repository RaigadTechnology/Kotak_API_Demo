# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 15:15:42 2021

@author: Sangram Phadke
"""
import datetime
from datetime import date
import numpy as np
import pandas as pd
import time
import random
import requests
import json
from io import StringIO #to convert string data in data frame
import kotakApi_UserLogin_Demo as kl #Importing the login page as this step will secure the login credential exp.

import ks_api_client
from ks_api_client import ks_api
# Defining the host is optional and defaults to https://tradeapi.kotaksecurities.com/apim
# See configuration.py for a list of all supported configuration parameters.

## FNO stocks symbols datafrme
df_symbol_file = pd.read_csv('FNO_Stocks.csv')

todaysdate = datetime.datetime.now().strftime("%d-%m-%Y")
kotak_todaysdate = datetime.datetime.now().strftime("%d_%m_%Y")
kotak_lastTradeDate = datetime.datetime.now().strftime("11_06_2021") ## Put last trading day date in format dd_mm_yyyy

#instrument_token Equity:
eq_it_url = 'https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_Cash_'+kotak_todaysdate+'.txt'  ## Replace kotak_todaysdate with kotak_lastTradeDate for testing
eq_it_req = requests.get(eq_it_url)
eq_it_text_data = eq_it_req.text

StringData = StringIO(eq_it_text_data)
df_eq_it = pd.read_csv(StringData, sep ="|")
    
## search for instrument_token and symbol matches with our symbol file
eq_it_list = []
for eqit in range(0,len(df_eq_it)):
    if df_eq_it.iloc[eqit][8] == 'EQ' and df_eq_it.iloc[eqit][9] == 'CASH' and df_eq_it.iloc[eqit][10] == 'NSE':
        if len(df_symbol_file.loc[df_symbol_file['Symbol'] == df_eq_it.iloc[eqit][1] ])==1:
            #print(df_eq_it.iloc[eqit][1])
            eq_it_list.append([df_eq_it.iloc[eqit][1],df_eq_it.iloc[eqit][0]])
df_eq_sy_it = pd.DataFrame(eq_it_list,columns=['Symbol','instrumentToken'])


# Get Report Orders
full_orders = kl.client.order_report()

# Get Report Orders for order id
#kl.client.order_report(order_id = "2210604000870")

##Live quote 
#kl.client.quote(instrument_token =7913)
pre_stockQuote = kl.client.quote(instrument_token =1900)
if len(pre_stockQuote) > 0:
    print("all ok")
else:
    print("error")
    
stockQuote_list = []
for qtnum in range(0,len(df_eq_sy_it)):
    #print(float(df_eq_sy_it.iloc[qtnum][1]))
    stockQuote = kl.client.quote(instrument_token = int(df_eq_sy_it.iloc[qtnum][1]))
    stockQuote_list.append(stockQuote)


fno_stockQuote_list = []
for index in range(0,len(stockQuote_list)):
    iltp = stockQuote_list[index]['success'][0]['ltp']
    ilnc = stockQuote_list[index]['success'][0]['lv_net_chg']
    ilncp = stockQuote_list[index]['success'][0]['lv_net_chg_perc']
    iop = stockQuote_list[index]['success'][0]['open_price']
    ihp = stockQuote_list[index]['success'][0]['high_price']
    ilp = stockQuote_list[index]['success'][0]['low_price']
    icp = stockQuote_list[index]['success'][0]['closing_price']
    iap = stockQuote_list[index]['success'][0]['average_trade_price']
    stock_name = stockQuote_list[index]['success'][0]['stk_name']
    #appended values
    fno_stockQuote_list.append([stock_name,iltp,ilnc,ilncp,iop,ihp,ilp,icp,iap])

df_stockQuote = pd.DataFrame(fno_stockQuote_list,columns=['Symbol','LTP','net_change','percent_change','Open_price','High_price','Low_price','Closing_price','Average_trade_price'])  

## Live full data
try:
    kl.client.history("LiveorEODHistorical",{"exchange":"NSE","co_code":"1900","period":"Y","cnt":"3"})
except Exception as e:
    print("Exception when calling Historical API->details: %s\n" % e)



# try:
#     # Place a Order
#     kl.client.place_order(order_type = "N", instrument_token = 1900,  \
#                     transaction_type = "SELL", quantity = 10, price = 0,\
#                     disclosed_quantity = 0, trigger_price = 0,\
#                     validity = "GFD", variety = "REGULAR", tag = "string")
# except Exception as e:
#     print("Exception when calling OrderApi->place_order: %s\n" % e)

# Get postion
    
todays_postion = kl.client.positions(position_type = "TODAYS")
#todays_postion['Success'][0]['realizedPL']  ## indexing list element

## Report
full_orders = kl.client.order_report()
#full_orders_list = []

##Details of Watchlist
#watchlist_list = kl.client.watchlists()


  
#instrument_token Derivatives:
# fno_it_url = 'https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_FNO_'+kotak_todaysdate+'.txt'  ## Replace kotak_todaysdate with kotak_ptd for testing
# fno_it_req = requests.get(fno_it_url)
# fno_it_text_data = fno_it_req.text

# StringData = StringIO(fno_it_text_data)
# df_fno_it = pd.read_csv(StringData, sep ="|")
# ## to peed up the data split the derivative dataframe

# ##Index datafrme
# df_flt_fno_NF = df_fno_it[(df_fno_it['instrumentName']=='NIFTY')]
# df_flt_fno_BN = df_fno_it[(df_fno_it['instrumentName']=='BANKNIFTY')]
# df_flt_fno_index = pd.concat([df_flt_fno_NF,df_flt_fno_BN])

## search for instrument_token and symbol matches for FNO order

# index_instrument = 'NIFTY' 
# expiry = '10JUN21'
# strike = 15500
# optionType = 'CE'

# fno_it_list = []
# for fnoit in range(0,len(df_flt_fno_index)):
#     if df_flt_fno_index.iloc[fnoit][9] == 'FO' and df_flt_fno_index.iloc[fnoit][10] == 'NSE':
#         if df_flt_fno_index.iloc[fnoit][1] == index_instrument and df_flt_fno_index.iloc[fnoit][5] == strike and df_flt_fno_index.iloc[fnoit][14] == 'CE' and df_flt_fno_index.iloc[fnoit][4] == expiry:
#             print(df_flt_fno_index.iloc[fnoit][1])
#             fno_it_list.append([df_flt_fno_index.iloc[fnoit][1],df_flt_fno_index.iloc[fnoit][5],df_flt_fno_index.iloc[fnoit][0],df_flt_fno_index.iloc[fnoit][4],df_flt_fno_index.iloc[fnoit][14]])
#             break
# df_fno_sy_it = pd.DataFrame(fno_it_list,columns=['Symbol','Strike','instrumentToken','Expiry','OptionType'])



##Terminate user's Session
#kl.client.logout()
