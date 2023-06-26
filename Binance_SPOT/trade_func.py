from binance.spot import Spot

# Generates Account Authentication
def binanceSpotkey(key, secret):
    c = Spot(api_key=key, api_secret=secret)
    return c

# Get Balance for Symbol/Asset
def BS_balance(c, coin):
    k = c.account()
    for i in range(len(k['balances'])):
        if(k['balances'][i]['asset']==coin):
            return (k['balances'][i]['free'])

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


# Check Decimals for Coin
def BS_check_precision(c, x):
    r = c.exchange_info(symbol=x)
    filters = r['symbols'][0]['filters']
    
    price_filter = None
    size_filter = None

    for type in filters:
        if type['filterType'] == 'PRICE_FILTER':
            price_filter = type
        elif type['filterType'] == 'LOT_SIZE':
            size_filter = type
    
    min_price = price_filter['minPrice'] if price_filter else None
    max_price = price_filter['maxPrice'] if price_filter else None
    min_qty = size_filter['minQty'] if size_filter else None
    max_qty = size_filter['maxQty'] if size_filter else None

    return min_price, max_price, min_qty, max_qty