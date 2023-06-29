from decimal import Decimal

def get_precision(c, coin, price, quantity, id):
    try:
        data = c.exchange_info(coin)['symbols'][0]
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
    except Exception as er:
        raise Exception('Precision Error: ',er)