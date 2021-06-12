# -*- coding: utf-8 -*-

import ks_api_client
from ks_api_client import ks_api
# Defining the host is optional and defaults to https://tradeapi.kotaksecurities.com/apim
# See configuration.py for a list of all supported configuration parameters.

## Kotak user access credentials 
access_code_id = "1234"  ## Daily access coode recived from SMS & Email

##Recived when user created via Email 
app_key_id ="ABCDEFGH123456789"   

##Fixed as per API 
access_token_id = "abcde-12345-abcd-1234-1234567"
consumer_key_id = "ABCDEFGH123456789"

## login code
client = ks_api.KSTradeApi(access_token = access_token_id , userid = "ABCD1234",consumer_key = consumer_key_id , ip = "127.0.0.1", app_id =app_key_id)

# Get session for user
client_login = client.login(password = "Abcde@1234")  

# client login data
userid_d = client_login["Success"]['userid']
message_d = client_login["Success"]['message']

#Generated session token
client_session = client.session_2fa(access_code = access_code_id)


##Terminate user's Session
#client.logout()