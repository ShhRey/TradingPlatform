from decimal import Decimal
from binance.spot import Spot
from binance.um_futures import UMFutures

def check_spot_precision(coin, price, quantity):
    try:
        c = Spot()
        data = c.exchange_info(coin)['symbols'][0]
        if data:
            precision = {}
            precision['price'] = Decimal(data['filters'][0]['tickSize'].find('1') - 1)
            price = Decimal(price).quantize(1/ 10 ** precision['price'])
            if int(float(data['filters'][1]['stepSize'])) == 1:
                precision['quantity'] = Decimal(data['filters'][1]['stepSize'])
                quantity = int(float(quantity))
            else:
                precision['quantity'] = Decimal(data['filters'][1]['stepSize']) 
                quantity = Decimal(quantity).quantize(precision['quantity'])
            return float(price), float(quantity)
        else:
            raise Exception('Invalid Coin Provided')
    except Exception as er:
        raise Exception('Precision Error: ',er)
    

def check_futures_precision(coin, price, quantity):
    try:
        c = UMFutures()
        data = c.exchange_info()['symbols']
        for symbols in data:
            if symbols['symbol'] == coin:
                precision = {}
                precision['price'] = Decimal(symbols['filters'][0]['tickSize'].find('1') - 1)
                price = Decimal(price).quantize(1/ 10 ** precision['price'])
                if int(float(symbols['filters'][1]['stepSize'])) == 1:
                    precision['quantity'] = Decimal(symbols['filters'][1]['stepSize'])
                    quantity = int(float(quantity))
                else:
                    precision['quantity'] = Decimal(symbols['filters'][1]['stepSize']) 
                    quantity = Decimal(quantity).quantize(precision['quantity'])
                return float(price), float(quantity)
    except Exception as er:
        raise Exception('Precision Error: ',er)