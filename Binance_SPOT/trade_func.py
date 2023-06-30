from binance.spot import Spot

# Generates Account Authentication
def binanceSpotkey(key, secret):
    c = Spot(api_key=key, api_secret=secret)
    return c

# Get Balance for API
def BS_API_Bal(c):
    assets = []
    asset_list = {}
    k = c.account()
    for i in range(len(k['balances'])):
        if (float(k['balances'][i]['free']) > 0):
            assets.append(k['balances'][i])
    for asset in assets:
        asset_list.update({asset['asset']: asset['free']})
    return asset_list

# Get Balance for Symbol/Asset
def BS_balance(c, asset):
    k = c.account()
    for i in range(len(k['balances'])):
        if (k['balances'][i]['asset']==asset):
            return k['balances'][i]['free']

# Place New Order
def BS_place_order(c, x, s, ot, q, pr = 0, tif='GTC'):
    if(ot == 'LIMIT'):
        r = c.new_order(symbol=x, side=s, type=ot, quantity=q, price=pr, timeInForce=tif)
    elif(ot == 'MARKET'):
        r = c.new_order(symbol=x, side=s, type =ot, quantity=q)
    else:
        raise Exception('Order Type Error!')
    return r

# Get all Open Orders for Symbol
def BS_open_orders(c, x):
    r = c.get_open_orders(symbol=x)
    return r

# Get order information of a Specific Order via OrderID
def BS_order_info(c, x, oid):
    r = c.get_order(symbol=x, orderId=oid)
    return r

# Get complete Trade History for Symbol
def BS_order_history(c, x):
    r = c.get_orders(symbol=x)
    return r

# Modify Current Order (Cancel the ongoing order and Place a New Order)
def BS_modify_order(c, x, s, ot, q, oid, pr=0, tif='GTC', cancelReplaceMode='STOP_ON_FAILURE'):
    r = c.cancel_and_replace(symbol=x, side=s, type=ot, quantity=q, price=pr, timeInForce=tif, cancelReplaceMode=cancelReplaceMode, cancelOrderId=oid)
    return r

# Cancel a specific open order 
def BS_delete_order(c, x, oid):
    r = c.cancel_order(symbol=x, orderId=oid)
    return r

# Cancel all open orders for Specific Symbol 
def BS_delete_all_orders(c, x):
    r = c.cancel_open_orders(symbol=x)
    return r