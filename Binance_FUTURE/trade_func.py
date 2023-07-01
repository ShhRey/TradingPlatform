from binance.um_futures import UMFutures

# ========================== Working APIs in Future ==================================
# Generates Authentication
def binanceFuturekey(key, secret):
    c = UMFutures(key=key, secret=secret)
    return c

# Get All Assets from API
def UMF_API_Bal(c):
    assets = {}
    k = c.balance()
    for i in range(len(k)):
        if (float(k[i]['maxWithdrawAmount']) > 0):
            assets.update({k[i]['asset']: k[i]['maxWithdrawAmount']})
    return assets

# Get Balance for Symbol/Asset
def UMF_balance(c, x):
    k = c.account()
    for i in range(len(k['assets'])):
        if(k['assets'][i]['asset']==x):
            return (k['assets'][i]['availableBalance'])

# Place New Order
def UMF_place_order(c, x, s, ot, q, pr = 0, tif='GTC', ps='BOTH'):
    if ((ot=='LIMIT') and ((ps=='BOTH') or (ps=='LONG') or (ps=='SHORT'))):
        print(ps)
        r = c.new_order(symbol=x, side = s, positionSide=ps, type = ot, quantity = q, price = pr, timeInForce = tif)
    elif (ot=='MARKET'):
        r = c.new_order(symbol=x, side = s, type = ot, quantity = q)
    else:
        raise Exception('Order Type Error!')
    return r

# Get all Open Orders for Symbol
def UMF_open_orders(c, x):
    r = c.get_orders(symbol=x)
    return r

# Get complete Trade History for Symbol
def UMF_order_history(c, x):
    r = c.get_all_orders(symbol = x)
    return r

# Cancel a specific open order 
def UMF_delete_order(c, x, oid):
    r = c.cancel_order(symbol = x, orderId = oid)
    return r

# Cancel all open orders for Specific Symbol
def UMF_delete_all_orders(c, x):
    r = c.cancel_open_orders(symbol=x)
    return r

# Modify Order Alternative (Cancel Order and Place New Order Combination)
def UMF_modify_order(c, x, s, ot, q, oid, pr, tif='GTC', ps='BOTH'):
    r = c.cancel_order(symbol=x, orderId=oid)
    if ((ot == 'LIMIT') and ((ps=='BOTH') or (ps=='LONG') or (ps=='SHORT'))):
        newr = c.new_order(symbol=x, side=s, positionSide=ps, type=ot, quantity=q, price=pr, timeInForce=tif)
        return r, newr
    elif(ot == 'MARKET'):
        newr = c.new_order(symbol=x, side=s, type=ot, quantity=q)
    else:
        raise Exception('Order Type Error!')

# Change Default Leverage Settings
def UMF_modify_leverage(c, x, l):
    r = c.change_leverage(symbol=x, leverage=l)
    return r


# ============================ Didnt Check These ==============================

def UMF_get_position_mode(c, x):
    r = c.get_position_mode(symbol=x)
    return r

def UMF_change_position_mode(c, x, dsp):
    r = c.change_position_mode(symbol=x, dualSidePosition=dsp)
    return r

def UMF_get_asset_mode(c, x):
    r = c.get_multi_asset_mode(symbol=x)
    return r


def UMF_change_asset_mode(c, x, mam):
    r = c.change_multi_asset_mode(symbol=x, multiAssetsMargin=mam)
    return r


def UMF_account_trades(c, x):
    r = c.get_account_trades(symbol=x)
    return r