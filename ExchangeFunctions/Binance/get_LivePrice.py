import requests

def live(x, exty):
    if (exty == 'SPOT'):
        while(True):
            try:
                key = "https://api.binance.com/api/v3/ticker/price?symbol=" + x
                data = requests.get(key)
                data = data.json()
                break
            except:
                continue        
        return data['price']
    
    elif (exty == 'UMFUTURE'):
        while(True):
            try:
                key ="https://fapi.binance.com/fapi/v1/ticker/price?symbol=" + x
                data = requests.get(key)
                data = data.json()
                break
            except:
                continue       
        return data['price']