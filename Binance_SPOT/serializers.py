from rest_framework import serializers
from Core.db import *
from Core.idgen import *
from Core.auth import *
import Core.telegram as tg
from ExchangeFunctions.Binance.check_Precision import check_precision
from ExchangeFunctions.Binance.min_OrdValue import spot_min_vol
from Binance_SPOT.trade_func import *

# Fetch API Asset Balance from Exchange
class GetLiveApiBalSerializer(serializers.Serializer):
    def func(self, validated_data):
        market = validated_data.get('market')
        exchange = validated_data.get('exchange')
        api_name = validated_data.get('api_name')

        if "jwt" not in validated_data or validated_data.get("jwt") == '':
            raise serializers.ValidationError('jwt is required and cannot be blank')
        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")
        
        if ('market' not in validated_data) or (market == ''):
            raise serializers.ValidationError('market is required and cannot be blank')
        exist_market = col4.find_one({'Name': market}, {'_id': 0})
        if not exist_market:
            raise serializers.ValidationError('Invalid market provided')
        
        if ('exchange' not in validated_data) or (exchange == ''):
            raise serializers.ValidationError('exchange is required and cannot be blank')
        exist_exchange = col5.find_one({'Name': exchange}, {'_id': 0})
        if not exist_exchange:
            raise serializers.ValidationError('Invalid exchange provided')
        
        if ('api_name' not in validated_data) or (api_name == ''):
            raise serializers.ValidationError('api_name is required and cannot be blank')
        exist_api = col6.find_one({'Name': api_name}, {'_id':0})
        try:
            client = binanceSpotkey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY'])
            api_bal = BS_API_Bal(c=client)
            return api_bal
        except:
            raise serializers.ValidationError('Invalid api_name provided')

# Fetch API Asset Balance from MongoDB
class GetDBApiBalSerializer(serializers.Serializer):
    def func(self, validated_data):
        market = validated_data.get('market')
        exchange = validated_data.get('exchange')
        api_name = validated_data.get('api_name')

        if "jwt" not in validated_data or validated_data.get("jwt") == '':
            raise serializers.ValidationError('jwt is required and cannot be blank')
        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")
        
        if ('market' not in validated_data) or (market == ''):
            raise serializers.ValidationError('market is required and cannot be blank')
        exist_market = col4.find_one({'Name': market}, {'_id': 0})
        if not exist_market:
            raise serializers.ValidationError('Invalid market provided')
        
        if ('exchange' not in validated_data) or (exchange == ''):
            raise serializers.ValidationError('exchange is required and cannot be blank')
        exist_exchange = col5.find_one({'Name': exchange}, {'_id': 0})
        if not exist_exchange:
            raise serializers.ValidationError('Invalid exchange provided')
        
        if ('api_name' not in validated_data) or (api_name == ''):
            raise serializers.ValidationError('api_name is required and cannot be blank')
        exist_api = col6.find_one({'Name': api_name}, {'_id':0})
        try:
            api_bal = exist_api['Balance']
            return api_bal
        except:
            raise serializers.ValidationError('Invalid api_name provided')

# View User's Open Orders
class ViewOpenOrderSerializer(serializers.Serializer):
    def func(self, validated_data):
        market = validated_data.get('market')
        exchange = validated_data.get('exchange')
        api_name = validated_data.get('api_name')
        coin = validated_data.get('coin')

        if "jwt" not in validated_data or validated_data.get("jwt") == '':
            raise serializers.ValidationError('jwt is required and cannot be blank')
        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")
        user = col1.find_one({'UserID': jwt_data['UserID']}, {'_id': 0})

        if ('market' not in validated_data) or (market == ''):
            raise serializers.ValidationError('market is required and cannot be blank')
        exist_market = col4.find_one({'Name': market}, {'_id': 0})
        if not exist_market:
            raise serializers.ValidationError('Invalid market provided')
        
        if ('exchange' not in validated_data) or (exchange == ''):
            raise serializers.ValidationError('exchange is required and cannot be blank')
        exist_exchange = col5.find_one({'Name': exchange}, {'_id': 0})
        if not exist_exchange:
            raise serializers.ValidationError('Invalid exchange provided')
        
        if ('api_name' not in validated_data) or (api_name == ''):
            raise serializers.ValidationError('api_name is required and cannot be blank')
        exist_api = col6.find_one({'Name': api_name}, {'_id':0})
        if not exist_api:
            raise serializers.ValidationError('Invalid api_name provided')
        
        if ('coin' not in validated_data) or coin == '':
            raise serializers.ValidationError('coin is required and cannot be blank')
        
        try:
            c = binanceSpotkey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY'])
            orders = BS_open_orders(c=c, x=coin)
        except:
            raise serializers.ValidationError('Invalid API Credentials')
        print(len(orders))
        if len(orders) == 0:
            raise serializers.ValidationError('No Open Orders Yet !')
        else:
            return orders
        
# Order History
class OrderHitorySerializer(serializers.Serializer):
    def func(self, validated_data):
        market = validated_data.get('market')
        exchange = validated_data.get('exchange')
        api_name = validated_data.get('api_name')
        coin = validated_data.get('coin')

        if "jwt" not in validated_data or validated_data.get("jwt") == '':
            raise serializers.ValidationError('jwt is required and cannot be blank')
        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")
        user = col1.find_one({'UserID': jwt_data['UserID']}, {'_id': 0})

        if ('market' not in validated_data) or (market == ''):
            raise serializers.ValidationError('market is required and cannot be blank')
        exist_market = col4.find_one({'Name': market}, {'_id': 0})
        if not exist_market:
            raise serializers.ValidationError('Invalid market provided')
        
        if ('exchange' not in validated_data) or (exchange == ''):
            raise serializers.ValidationError('exchange is required and cannot be blank')
        exist_exchange = col5.find_one({'Name': exchange}, {'_id': 0})
        if not exist_exchange:
            raise serializers.ValidationError('Invalid exchange provided')
        
        if ('api_name' not in validated_data) or (api_name == ''):
            raise serializers.ValidationError('api_name is required and cannot be blank')
        exist_api = col6.find_one({'Name': api_name}, {'_id':0})
        if not exist_api:
            raise serializers.ValidationError('Invalid api_name provided')
        
        if ('coin' not in validated_data) or coin == '':
            raise serializers.ValidationError('coin is required and cannot be blank')
        
        try:
            c = binanceSpotkey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY'])
            orders = BS_order_history(c=c, x=coin)
        except:
            raise serializers.ValidationError('Invalid API Credentials')
        if len(orders) == 0:
            raise serializers.ValidationError('No Orders Placed on this Coin !')
        else:
            return orders

# Place New Limit BUY Order
class PlaceLimitBuySerializer(serializers.Serializer):
    def func(self, validated_data):
        market = validated_data.get('market')
        exchange = validated_data.get('exchange')
        api_name = validated_data.get('api_name')
        coin = validated_data.get('coin')
        price = validated_data.get('price')
        quantity = validated_data.get('quantity')

        if "jwt" not in validated_data or validated_data.get("jwt") == '':
            raise serializers.ValidationError('jwt is required and cannot be blank')
        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")
        user = col1.find_one({'UserID': jwt_data['UserID']}, {'_id': 0})
        
        if ('market' not in validated_data) or (market == ''):
            raise serializers.ValidationError('market is required and cannot be blank')
        exist_market = col4.find_one({'Name': market}, {'_id': 0})
        if not exist_market:
            raise serializers.ValidationError('Invalid market provided')
        
        if ('exchange' not in validated_data) or (exchange == ''):
            raise serializers.ValidationError('exchange is required and cannot be blank')
        exist_exchange = col5.find_one({'Name': exchange}, {'_id': 0})
        if not exist_exchange:
            raise serializers.ValidationError('Invalid exchange provided')
        
        if ('api_name' not in validated_data) or (api_name == ''):
            raise serializers.ValidationError('api_name is required and cannot be blank')
        exist_api = col6.find_one({'Name': api_name}, {'_id':0})
        if not exist_api:
            raise serializers.ValidationError('Invalid api_name provided')
        
        if ('coin' not in validated_data) or coin == '':
            raise serializers.ValidationError('coin is required and cannot be blank')
        
        if ('price' not in validated_data) or price == '':
            raise serializers.ValidationError('price is required and cannot be blank')
        
        if ('quantity' not in validated_data) or quantity == '':
            raise serializers.ValidationError('quantity is required and cannot be blank')

        try:
            pre_values = check_precision(coin=coin, price=price, quantity=quantity)
            upd_price = pre_values[0]
            upd_quantity = pre_values[1]
            c = binanceSpotkey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY'])
            
            if spot_min_vol(coin=coin) <= (float(upd_price) * float(upd_quantity)):
                order = BS_place_order(c=c, x=coin, s='BUY', ot='LIMIT', pr=upd_price, q=upd_quantity)
                print(order)
                col8.insert_one({
                    'OrderID': str(order['orderId']),
                    'OrderTime': dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    'Coin': order['symbol'],
                    'OrderType': order['type'],
                    'Side': order['side'],
                    'OrderPrice': order['price'],
                    'OrderQty': order['origQty'],
                    'ExecQty': order['executedQty'],
                    'CummQuoteQty': order['cummulativeQuoteQty'],
                    'Status': order['status'],
                    'TimeInForce': order['timeInForce'],
                    'OrderedVia': 'API',
                })
                tg.send(f"Limit BUY Order Placed on Binance by {user['UserName']} via API: {exist_api['Name']}")
                return order
        except:
            raise serializers.ValidationError('Order Could not be Placed')
        
# Place New Limit SELL Order
class PlaceLimitSellSerializer(serializers.Serializer):
    def func(self, validated_data):
        market = validated_data.get('market')
        exchange = validated_data.get('exchange')
        api_name = validated_data.get('api_name')
        coin = validated_data.get('coin')
        price = validated_data.get('price')
        quantity = validated_data.get('quantity')

        if "jwt" not in validated_data or validated_data.get("jwt") == '':
            raise serializers.ValidationError('jwt is required and cannot be blank')
        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")
        user = col1.find_one({'UserID': jwt_data['UserID']}, {'_id': 0})
        
        if ('market' not in validated_data) or (market == ''):
            raise serializers.ValidationError('market is required and cannot be blank')
        exist_market = col4.find_one({'Name': market}, {'_id': 0})
        if not exist_market:
            raise serializers.ValidationError('Invalid market provided')
        
        if ('exchange' not in validated_data) or (exchange == ''):
            raise serializers.ValidationError('exchange is required and cannot be blank')
        exist_exchange = col5.find_one({'Name': exchange}, {'_id': 0})
        if not exist_exchange:
            raise serializers.ValidationError('Invalid exchange provided')
        
        if ('api_name' not in validated_data) or (api_name == ''):
            raise serializers.ValidationError('api_name is required and cannot be blank')
        exist_api = col6.find_one({'Name': api_name}, {'_id':0})
        if not exist_api:
            raise serializers.ValidationError('Invalid api_name provided')
        
        if ('coin' not in validated_data) or coin == '':
            raise serializers.ValidationError('coin is required and cannot be blank')
        
        if ('price' not in validated_data) or price == '':
            raise serializers.ValidationError('price is required and cannot be blank')
        
        if ('quantity' not in validated_data) or quantity == '':
            raise serializers.ValidationError('quantity is required and cannot be blank')

        try:
            pre_values = check_precision(coin=coin, price=price, quantity=quantity)
            upd_price = pre_values[0]
            upd_quantity = pre_values[1]
            c = binanceSpotkey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY'])
            
            if spot_min_vol(coin=coin) <= (float(upd_price) * float(upd_quantity)):
                order = BS_place_order(c=c, x=coin, s='SELL', ot='LIMIT', pr=upd_price, q=upd_quantity)
                print(order)
                col8.insert_one({
                    'OrderID': str(order['orderId']),
                    'OrderTime': dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    'Coin': order['symbol'],
                    'OrderType': order['type'],
                    'Side': order['side'],
                    'OrderPrice': order['price'],
                    'OrderQty': order['origQty'],
                    'ExecQty': order['executedQty'],
                    'CummQuoteQty': order['cummulativeQuoteQty'],
                    'Status': order['status'],
                    'TimeInForce': order['timeInForce'],
                    'OrderedVia': 'API',
                })
                tg.send(f"Limit SELL Order Placed on Binance by {user['UserName']} via API: {exist_api['Name']}")
                return order
        except:
            raise serializers.ValidationError('Order Could not be Placed')
        
# Place New Market BUY Order
class PlaceMarketBuySerializer(serializers.Serializer):
    def func(self, validated_data):
        market = validated_data.get('market')
        exchange = validated_data.get('exchange')
        api_name = validated_data.get('api_name')
        coin = validated_data.get('coin')
        price = validated_data.get('price')
        quantity = validated_data.get('quantity')

        if "jwt" not in validated_data or validated_data.get("jwt") == '':
            raise serializers.ValidationError('jwt is required and cannot be blank')
        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")
        user = col1.find_one({'UserID': jwt_data['UserID']}, {'_id': 0})
        
        if ('market' not in validated_data) or (market == ''):
            raise serializers.ValidationError('market is required and cannot be blank')
        exist_market = col4.find_one({'Name': market}, {'_id': 0})
        if not exist_market:
            raise serializers.ValidationError('Invalid market provided')
        
        if ('exchange' not in validated_data) or (exchange == ''):
            raise serializers.ValidationError('exchange is required and cannot be blank')
        exist_exchange = col5.find_one({'Name': exchange}, {'_id': 0})
        if not exist_exchange:
            raise serializers.ValidationError('Invalid exchange provided')
        
        if ('api_name' not in validated_data) or (api_name == ''):
            raise serializers.ValidationError('api_name is required and cannot be blank')
        exist_api = col6.find_one({'Name': api_name}, {'_id':0})
        if not exist_api:
            raise serializers.ValidationError('Invalid api_name provided')
        
        if ('coin' not in validated_data) or coin == '':
            raise serializers.ValidationError('coin is required and cannot be blank')
        
        if ('quantity' not in validated_data) or quantity == '':
            raise serializers.ValidationError('quantity is required and cannot be blank')

        try:
            pre_values = check_precision(coin=coin, price=price, quantity=quantity)
            upd_price = pre_values[0]
            upd_quantity = pre_values[1]
            c = binanceSpotkey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY'])
            
            if spot_min_vol(coin=coin) <= (float(upd_price) * float(upd_quantity)):
                order = BS_place_order(c=c, x=coin, s='BUY', ot='MARKET', q=upd_quantity)
                print(order)
                col8.insert_one({
                    'OrderID': str(order['orderId']),
                    'OrderTime': dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    'Coin': order['symbol'],
                    'OrderType': order['type'],
                    'Side': order['side'],
                    'OrderPrice': order['price'],
                    'OrderQty': order['origQty'],
                    'ExecQty': order['executedQty'],
                    'CummQuoteQty': order['cummulativeQuoteQty'],
                    'Status': order['status'],
                    'TimeInForce': order['timeInForce'],
                    'OrderedVia': 'API',
                })
                tg.send(f"Market BUY Order Placed on Binance by {user['UserName']} via API: {exist_api['Name']}")
                return order
        except:
            raise serializers.ValidationError('Order Could not be Placed')

# Place New Market SELL Order
class PlaceMarketSellSerializer(serializers.Serializer):
    def func(self, validated_data):
        market = validated_data.get('market')
        exchange = validated_data.get('exchange')
        api_name = validated_data.get('api_name')
        coin = validated_data.get('coin')
        price = validated_data.get('price')
        quantity = validated_data.get('quantity')

        if "jwt" not in validated_data or validated_data.get("jwt") == '':
            raise serializers.ValidationError('jwt is required and cannot be blank')
        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")
        user = col1.find_one({'UserID': jwt_data['UserID']}, {'_id': 0})
        
        if ('market' not in validated_data) or (market == ''):
            raise serializers.ValidationError('market is required and cannot be blank')
        exist_market = col4.find_one({'Name': market}, {'_id': 0})
        if not exist_market:
            raise serializers.ValidationError('Invalid market provided')
        
        if ('exchange' not in validated_data) or (exchange == ''):
            raise serializers.ValidationError('exchange is required and cannot be blank')
        exist_exchange = col5.find_one({'Name': exchange}, {'_id': 0})
        if not exist_exchange:
            raise serializers.ValidationError('Invalid exchange provided')
        
        if ('api_name' not in validated_data) or (api_name == ''):
            raise serializers.ValidationError('api_name is required and cannot be blank')
        exist_api = col6.find_one({'Name': api_name}, {'_id':0})
        if not exist_api:
            raise serializers.ValidationError('Invalid api_name provided')
        
        if ('coin' not in validated_data) or coin == '':
            raise serializers.ValidationError('coin is required and cannot be blank')
        
        if ('quantity' not in validated_data) or quantity == '':
            raise serializers.ValidationError('quantity is required and cannot be blank')

        try:
            pre_values = check_precision(coin=coin, price=price, quantity=quantity)
            upd_price = pre_values[0]
            upd_quantity = pre_values[1]
            c = binanceSpotkey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY'])
            
            if spot_min_vol(coin=coin) <= (float(upd_price) * float(upd_quantity)):
                order = BS_place_order(c=c, x=coin, s='SELL', ot='MARKET', q=upd_quantity)
                print(order)
                col8.insert_one({
                    'OrderID': str(order['orderId']),
                    'OrderTime': dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    'Coin': order['symbol'],
                    'OrderType': order['type'],
                    'Side': order['side'],
                    'OrderPrice': order['price'],
                    'OrderQty': order['origQty'],
                    'ExecQty': order['executedQty'],
                    'CummQuoteQty': order['cummulativeQuoteQty'],
                    'Status': order['status'],
                    'TimeInForce': order['timeInForce'],
                    'OrderedVia': 'API',
                })
                tg.send(f"Market SELL Order Placed on Binance by {user['UserName']} via API: {exist_api['Name']}")
                return order
        except:
            raise serializers.ValidationError('Order Could not be Placed')