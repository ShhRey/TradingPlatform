from binance.um_futures import UMFutures
from binance.spot import Spot
import time

#============== Generate Listen Key for Binance Future ==================#
def generate_UMF_ListenKey(key, secret):
    fc = UMFutures(key=key, secret=secret)
    listen_key_info = fc.new_listen_key()
    listen_key = listen_key_info['listenKey']
    return listen_key

#================== Generate Listen Key for Binance Spot =========================#
def generate_BS_ListenKey(key, secret):
    sc = Spot(api_key=key, api_secret=secret)
    listen_key_info = sc.new_listen_key()
    listen_key = listen_key_info['listenKey']
    return listen_key

#======================= Update Listen Key for SPOT / FUTURE =======================#
def update_ListenKey(key, secret, exchange, listen_key):
    if exchange == 'SPOT':
        c = UMFutures(key=key, secret=secret)
    elif exchange == 'FUTURE':
        c = Spot(api_key=key, api_secret=secret)
    listen_key_info = ''

    if 'code' in listen_key_info and listen_key_info['code'] == -2015:
        print('Listen Key Expired. Creating a new one.....')
        listen_key_info = c.new_listen_key()
        listen_key = listen_key_info['listenKey']
    else:
        listen_key_info = c.renew_listen_key(listenKey=listen_key)
        listen_key = listen_key
    
    return listen_key
    

# Integrating Functionality for Websocket to Check / Update ListenKey for Particular User
# my_api_key = ''
# my_secret_key = ''
# listen_key = None
# exchange = str(input('Enter Exchange: '))

# while True:
#     if exchange == 'SPOT':
#         fk = generate_UMF_ListenKey(key=my_api_key, secret=my_secret_key)
#         print(fk)
#         time.sleep(10)
#         uk = update_ListenKey(key=my_api_key, secret=my_secret_key, listen_key=fk)
        

#     elif exchange == 'FUTURE':
#         sk = generate_BS_ListenKey(key=my_api_key, secret=my_secret_key)
#         print(sk)
#         time.sleep(10)
#         uk = update_ListenKey(key=my_api_key, secret=my_secret_key, listen_key=sk)
#         print(uk)

#     else:
#         raise Exception('Invalid Exchange Provided')
