import re
from ExchangeFunctions.Binance.get_LivePrice import live as glp
from binance.client import Client

ct = Client()

def spot_min_vol(coin):
    match = re.search(r"(.*?)(BTC|USDT|BUSD|ETH|BNB)$", coin)
    if(match.group(2)=='USDT'):
        return 10
    elif(match.group(2)=='BUSD'):
        return 10/float(glp('BUSDUSDT', 'SPOT'))
    elif(match.group(2)=='ETH'):
        return 10/float(glp('ETHUSDT', 'SPOT'))
    elif(match.group(2)=='BTC'):
        return 10/float(glp('BTCUSDT', 'SPOT'))
    elif(match.group(2)=='BNB'):
        return 10/float(glp('BNBUSDT', 'SPOT'))
    else:
        return 0
    

def future_min_vol(coin):
    match = re.search(r"(.*?)(BTC|USDT|BUSD|ETH|BNB)$", coin)
    if(match.group(2)=='USDT'):
        return 10
    elif(match.group(2)=='BUSD'):
        return 10/float(glp('BUSDUSDT', 'UMFUTURE'))
    elif(match.group(2)=='ETH'):
        return 10/float(glp('ETHUSDT', 'UMFUTURE'))
    elif(match.group(2)=='BTC'):
        return 10/float(glp('BTCUSDT', 'UMFUTURE'))
    elif(match.group(2)=='BNB'):
        return 10/float(glp('BNBUSDT', 'UMFUTURE'))
    else:
        return 0