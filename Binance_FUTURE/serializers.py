from rest_framework import serializers
from Core.db import *
from Core.idgen import *
from Core.auth import *
import Core.telegram as tg
from ExchangeFunctions.Binance.check_Precision import check_futures_precision
from ExchangeFunctions.Binance.min_OrdValue import future_min_vol
from Binance_FUTURE.trade_func import *

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
        exist_api = col6.find_one({'Name': api_name, 'created_by.UserID': jwt_data['UserID']}, {'_id':0})
        print(exist_api)
        try:
            client = binanceFuturekey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY'])
            api_bal = UMF_API_Bal(c=client)
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
        exist_api = col6.find_one({'Name': api_name, 'created_by.UserID': jwt_data['UserID']}, {'_id':0})
        try:
            api_bal = exist_api['Balance']
            return api_bal
        except:
            raise serializers.ValidationError('Invalid api_name provided')

# Get PositionMode for API
class GetPositionModeSerializer(serializers.Serializer):
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
        if exchange != 'Binance_FUTURE':
            raise serializers.ValidationError('PositionMode is supported only in Binance_FUTURES')
        
        if ('api_name' not in validated_data) or (api_name == ''):
            raise serializers.ValidationError('api_name is required and cannot be blank')
        exist_api = col6.find_one({'Name': api_name, 'Exchange': exchange, 'created_by.UserID': jwt_data['UserID']}, {'_id':0})
        try:
            posi_mode = UMF_get_position_mode(c=binanceFuturekey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY']))
            if posi_mode:
                posi_mode = str(posi_mode['dualSidePosition'])
                col6.update_one({'Name': api_name, 'Exchange': exchange, 'created_by.UserID': jwt_data['UserID']}, {'$set': {'Settings.PositionMode': posi_mode}})
                return posi_mode
            else:
                raise serializers.ValidationError('PositionMode not set for API')
        except:
            raise serializers.ValidationError('Invalid api_name provided')

# Change PositionMode for User API
class ChangePositionModeSerializer(serializers.Serializer):
    def func(self, validated_data):
        market = validated_data.get('market')
        exchange = validated_data.get('exchange')
        api_name = validated_data.get('api_name')
        position = str(validated_data.get('position'))

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
        if exchange != 'Binance_FUTURE':
            raise serializers.ValidationError('PositionMode is supported only in Binance_FUTURES')
        
        if ('api_name' not in validated_data) or (api_name == ''):
            raise serializers.ValidationError('api_name is required and cannot be blank')
        exist_api = col6.find_one({'Name': api_name, 'Exchange': exchange, 'created_by.UserID': jwt_data['UserID']}, {'_id':0})

        if ('position' not in validated_data) or (position == ''):
            raise serializers.ValidationError('position is required and cannot be blank')
        if position not in ('True', 'False'):
            raise serializers.ValidationError('position only accepts either True or False')
        if (position == exist_api['Settings']['PositionMode']):
            raise serializers.ValidationError('No need to change position')
        try:
            c = binanceFuturekey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY']) 
            change_mode = UMF_change_position_mode(c=c, dsp=position)
            if change_mode['dualSidePosition']:
                change_mode = str(change_mode['dualSidePosition'])
                col6.update_one({'Name': api_name, 'Exchange': exchange, 'created_by.UserID': jwt_data['UserID']}, {'$set': {'PositionMode': change_mode}})
                return change_mode  
        except:
            raise serializers.ValidationError('Currently PositionMode cannot be changed')

# Get AssetMode for API
class GetAssetModeSerializer(serializers.Serializer):
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
        if exchange != 'Binance_FUTURE':
            raise serializers.ValidationError('PositionMode is supported only in Binance_FUTURES')
        
        if ('api_name' not in validated_data) or (api_name == ''):
            raise serializers.ValidationError('api_name is required and cannot be blank')
        exist_api = col6.find_one({'Name': api_name, 'Exchange': exchange, 'created_by.UserID': jwt_data['UserID']}, {'_id':0})
        try:
            asset_mode = UMF_get_asset_mode(c=binanceFuturekey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY']))
            print(asset_mode)
            if asset_mode:
                asset_mode = str(asset_mode['multiAssetsMargin'])
                col6.update_one({'Name': api_name, 'Exchange': exchange, 'created_by.UserID': jwt_data['UserID']}, {'$set': {'Settings.MultiAssetMode': asset_mode}})
                return asset_mode
            else:
                raise serializers.ValidationError('MultiAssetMode not set for API')
        except:
            raise serializers.ValidationError('Invalid api_name provided')

# Change AssetMode for User API
class ChangeAssetModeSerializer(serializers.Serializer):
    def func(self, validated_data):
        market = validated_data.get('market')
        exchange = validated_data.get('exchange')
        api_name = validated_data.get('api_name')
        asset = str(validated_data.get('asset'))

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
        if exchange != 'Binance_FUTURE':
            raise serializers.ValidationError('AssetMode is supported only in Binance_FUTURES')
        
        if ('api_name' not in validated_data) or (api_name == ''):
            raise serializers.ValidationError('api_name is required and cannot be blank')
        exist_api = col6.find_one({'Name': api_name, 'Exchange': exchange, 'created_by.UserID': jwt_data['UserID']}, {'_id':0})

        if ('asset' not in validated_data) or (asset == ''):
            raise serializers.ValidationError('asset is required and cannot be blank')
        if asset not in ('True', 'False'):
            raise serializers.ValidationError('asset only accepts either True or False')
        if (asset == exist_api['Settings']['MultiAssetMode']):
            raise serializers.ValidationError('No need to change asset')
        try:
            c = binanceFuturekey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY']) 
            change_mode = UMF_change_asset_mode(c=c, mam=asset)
            if change_mode['code'] == 200 and change_mode['msg'] == 'success':
                change_mode = asset
                col6.update_one({'Name': api_name, 'Exchange': exchange, 'created_by.UserID': jwt_data['UserID']}, {'$set': {'Settings.MultiAssetMode': change_mode}})
                return change_mode  
        except:
            raise serializers.ValidationError('Currently AssetMode cannot be changed')

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
        exist_api = col6.find_one({'Name': api_name, 'created_by.UserID': user['UserID']}, {'_id':0})
        if not exist_api:
            raise serializers.ValidationError('Invalid api_name provided')
        
        if ('coin' not in validated_data) or coin == '':
            raise serializers.ValidationError('coin is required and cannot be blank')
        
        try:
            c = binanceFuturekey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY'])
            orders = UMF_open_orders(c=c, x=coin)
        except:
            raise serializers.ValidationError('Invalid API Credentials')
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
            c = binanceFuturekey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY'])
            orders = UMF_order_history(c=c, x=coin)
        except:
            raise serializers.ValidationError('Invalid API ')
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
        exist_api = col6.find_one({'Name': api_name, 'Exchange': exchange, 'Type':'LIVE', 'Status': 'ACTIVE', 'created_by.UserID': user['UserID']}, {'_id':0})
        if not exist_api:
            raise serializers.ValidationError('Invalid api_name provided / API Inactive')
        
        if ('coin' not in validated_data) or coin == '':
            raise serializers.ValidationError('coin is required and cannot be blank')
        
        if ('price' not in validated_data) or price == '':
            raise serializers.ValidationError('price is required and cannot be blank')
        
        if ('quantity' not in validated_data) or quantity == '':
            raise serializers.ValidationError('quantity is required and cannot be blank')
        
        if exist_api['Settings']['PositionMode'] == 'True':
            posi_side = validated_data.get('posi_side')
            if ('posi_side' not in validated_data) or (posi_side == ''):
                raise serializers.ValidationError('API set for HEDGE. posi_side is required and cannot be blank')
            if posi_side not in ('LONG', 'SHORT'):
                raise serializers.ValidationError('posi_side only accepts either LONG or SHORT')
        else:
            posi_side = 'BOTH'

        try:
            pre_values = check_futures_precision(coin=coin, price=price, quantity=quantity)
            upd_price = pre_values[0]
            upd_quantity = pre_values[1]
            c = binanceFuturekey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY'])
            
            if future_min_vol(coin=coin) <= (float(upd_price) * float(upd_quantity)):
                order = UMF_place_order(c=c, x=coin, s='BUY', ot='LIMIT', pr=upd_price, q=upd_quantity, ps=posi_side)
                print(order)
                col9.insert_one({
                    'OrderID': str(order['orderId']),
                    'OrderTime': str(order['updateTime']),
                    'Coin': order['symbol'],
                    'OrderType': order['type'],
                    'Side': order['side'],
                    'PositionSide': order['positionSide'],
                    'OrderPrice': order['price'],
                    'OrderQty': order['origQty'],
                    'ExecQty': order['executedQty'],
                    'CummQuoteQty': order['cumQty'],
                    'Status': order['status'],
                    'TimeInForce': order['timeInForce'],
                    'UserID': user['UserID'],
                    'ApiID': exist_api['ApiID'],
                    'OrderedVia': 'MANUAL',
                })
                tg.send(f"Limit BUY Order Placed on {exchange} by {user['UserName']} via API: {exist_api['Name']}")
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
        exist_api = col6.find_one({'Name': api_name, 'Exchange': exchange, 'Type':'LIVE', 'Status': 'ACTIVE', 'created_by.UserID': user['UserID']}, {'_id':0})
        if not exist_api:
            raise serializers.ValidationError('Invalid api_name provided / API Inactive')
        
        if ('coin' not in validated_data) or coin == '':
            raise serializers.ValidationError('coin is required and cannot be blank')
        
        if ('price' not in validated_data) or price == '':
            raise serializers.ValidationError('price is required and cannot be blank')
        
        if ('quantity' not in validated_data) or quantity == '':
            raise serializers.ValidationError('quantity is required and cannot be blank')
        
        try: 
            if exist_api['Settings']['PositionMode'] == 'True':
                posi_side = validated_data.get('posi_side')
                if ('posi_side' not in validated_data) or (posi_side == ''):
                    raise serializers.ValidationError('API set for HEDGE. posi_side is required and cannot be blank')
                if posi_side not in ('LONG', 'SHORT'):
                    raise serializers.ValidationError('posi_side only accepts either LONG or SHORT')
            else:
                posi_side = 'BOTH'
        except:
            raise serializers.ValidationError('PositionMode cannot be Changed')

        try:
            pre_values = check_futures_precision(coin=coin, price=price, quantity=quantity)
            upd_price = pre_values[0]
            upd_quantity = pre_values[1]
            c = binanceFuturekey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY'])
            
            if future_min_vol(coin=coin) <= (float(upd_price) * float(upd_quantity)):
                order = UMF_place_order(c=c, x=coin, s='SELL', ot='LIMIT', pr=upd_price, q=upd_quantity, ps=posi_side)
                print(order)
                col9.insert_one({
                    'OrderID': str(order['orderId']),
                    'OrderTime': str(order['updateTime']),
                    'Coin': order['symbol'],
                    'OrderType': order['type'],
                    'Side': order['side'],
                    'PositionSide': order['positionSide'],
                    'OrderPrice': order['price'],
                    'OrderQty': order['origQty'],
                    'ExecQty': order['executedQty'],
                    'CummQuoteQty': order['cumQty'],
                    'Status': order['status'],
                    'TimeInForce': order['timeInForce'],
                    'UserID': user['UserID'],
                    'ApiID': exist_api['ApiID'],
                    'OrderedVia': 'MANUAL',
                })
                tg.send(f"Limit SELL Order Placed on {exchange} by {user['UserName']} via API: {exist_api['Name']}")
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
        exist_api = col6.find_one({'Name': api_name, 'Exchange': exchange, 'Type':'LIVE', 'Status': 'ACTIVE', 'created_by.UserID': user['UserID']}, {'_id':0})
        if not exist_api:
            raise serializers.ValidationError('Invalid api_name provided / API Inactive')
        
        if ('coin' not in validated_data) or coin == '':
            raise serializers.ValidationError('coin is required and cannot be blank')
        
        if ('quantity' not in validated_data) or quantity == '':
            raise serializers.ValidationError('quantity is required and cannot be blank')
        
        try: 
            if exist_api['Settings']['PositionMode'] == 'True':
                posi_side = validated_data.get('posi_side')
                if ('posi_side' not in validated_data) or (posi_side == ''):
                    raise serializers.ValidationError('API set for HEDGE. posi_side is required and cannot be blank')
                if posi_side not in ('LONG', 'SHORT'):
                    raise serializers.ValidationError('posi_side only accepts either LONG or SHORT')
            else:
                posi_side = 'BOTH'
        except:
            raise serializers.ValidationError('PositionMode cannot be Changed')

        try:
            pre_values = check_futures_precision(coin=coin, price=price, quantity=quantity)
            upd_price = pre_values[0]
            upd_quantity = pre_values[1]
            c = binanceFuturekey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY'])
            
            if future_min_vol(coin=coin) <= (float(upd_price) * float(upd_quantity)):
                order = UMF_place_order(c=c, x=coin, s='BUY', ot='MARKET', q=upd_quantity)
                print(order)
                col9.insert_one({
                    'OrderID': str(order['orderId']),
                    'OrderTime': str(order['updateTime']),
                    'Coin': order['symbol'],
                    'OrderType': order['type'],
                    'Side': order['side'],
                    'PositionSide': order['positionSide'],
                    'OrderPrice': order['price'],
                    'OrderQty': order['origQty'],
                    'ExecQty': order['executedQty'],
                    'CummQuoteQty': order['cumQty'],
                    'Status': order['status'],
                    'TimeInForce': order['timeInForce'],
                    'UserID': user['UserID'],
                    'ApiID': exist_api['ApiID'],
                    'OrderedVia': 'MANUAL',
                })
                tg.send(f"Market BUY Order Placed on {exchange} by {user['UserName']} via API: {exist_api['Name']}")
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
        exist_api = col6.find_one({'Name': api_name, 'Exchange': exchange, 'Type':'LIVE', 'Status': 'ACTIVE', 'created_by.UserID': user['UserID']}, {'_id':0})
        if not exist_api:
            raise serializers.ValidationError('Invalid api_name provided / API Inactive')
        
        if ('coin' not in validated_data) or coin == '':
            raise serializers.ValidationError('coin is required and cannot be blank')
        
        if ('quantity' not in validated_data) or quantity == '':
            raise serializers.ValidationError('quantity is required and cannot be blank')
        
        try: 
            if exist_api['Settings']['PositionMode'] == 'True':
                posi_side = validated_data.get('posi_side')
                if ('posi_side' not in validated_data) or (posi_side == ''):
                    raise serializers.ValidationError('API set for HEDGE. posi_side is required and cannot be blank')
                if posi_side not in ('LONG', 'SHORT'):
                    raise serializers.ValidationError('posi_side only accepts either LONG or SHORT')
            else:
                posi_side = 'BOTH'
        except:
            raise serializers.ValidationError('PositionMode cannot be Changed')

        try:
            pre_values = check_futures_precision(coin=coin, price=price, quantity=quantity)
            upd_price = pre_values[0]
            upd_quantity = pre_values[1]
            c = binanceFuturekey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY'])
            
            if future_min_vol(coin=coin) <= (float(upd_price) * float(upd_quantity)):
                order = UMF_place_order(c=c, x=coin, s='SELL', ot='MARKET', q=upd_quantity, ps=posi_side)
                print(order)
                col9.insert_one({
                    'OrderID': str(order['orderId']),
                    'OrderTime': str(order['updateTime']),
                    'Coin': order['symbol'],
                    'OrderType': order['type'],
                    'Side': order['side'],
                    'PositionSide': order['positionSide'],
                    'OrderPrice': order['price'],
                    'OrderQty': order['origQty'],
                    'ExecQty': order['executedQty'],
                    'CummQuoteQty': order['cumQty'],
                    'Status': order['status'],
                    'TimeInForce': order['timeInForce'],
                    'UserID': user['UserID'],
                    'ApiID': exist_api['ApiID'],
                    'OrderedVia': 'MANUAL',
                })
                tg.send(f"Market SELL Order Placed on {exchange} by {user['UserName']} via API: {exist_api['Name']}")
                return order
        except:
            raise serializers.ValidationError('Order Could not be Placed')

# Modify Open Order
class ModifyOrderSerializer(serializers.Serializer):
    def func(self, validated_data):
        market = validated_data.get('market')
        exchange = validated_data.get('exchange')
        api_name = validated_data.get('api_name')
        orderid = validated_data.get('orderid')
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
        exist_api = col6.find_one({'Name': api_name, 'Exchange': exchange, 'Type':'LIVE', 'Status': 'ACTIVE', 'created_by.UserID': user['UserID']}, {'_id':0})
        if not exist_api:
            raise serializers.ValidationError('Invalid api_name provided / API Inactive')
        
        if ('coin' not in validated_data) or coin == '':
            raise serializers.ValidationError('coin is required and cannot be blank')
        
        if ('price' not in validated_data) or price == '':
            raise serializers.ValidationError('price is required and cannot be blank')
        
        if ('quantity' not in validated_data) or quantity == '':
            raise serializers.ValidationError('quantity is required and cannot be blank')
        
        if ('orderid' not in validated_data) or orderid == '':
            raise serializers.ValidationError('orderid is required and cannot be blank')
        

        exist_order = col9.find_one({'OrderID': orderid, 'Coin': coin, 'Status': 'NEW', 'UserID': user['UserID'], 'ApiID': exist_api['ApiID']}, {'_id': 0})
        if not exist_order:
            raise serializers.ValidationError('Order not Found')
        if (float(exist_order['OrderPrice']) == float(price)) and (float(exist_order['OrderQty']) == float(quantity)):
            raise serializers.ValidationError('Cannot modify order with same values')
        try:
            pre_values = check_futures_precision(coin=coin, price=price, quantity=quantity)
            upd_price = float(pre_values[0])
            upd_quantity = float(pre_values[1])
            c = binanceFuturekey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY'])
            if future_min_vol(coin=coin) <= (upd_price * upd_quantity):
                mod_order = UMF_modify_order(c=c, oid=orderid, x=coin, s=exist_order['Side'], ot=exist_order['OrderType'], q=upd_quantity, pr=upd_price, ps=exist_order['PositionSide'])
                col9.update_one({'OrderID': orderid, 'Coin': coin, 'Status': 'NEW', 'UserID': user['UserID'], 'ApiID': exist_api['ApiID']}, {'$set': {'Status': 'CANCELED'}})
                col9.insert_one({
                    'OrderID': str(mod_order[1]['orderId']), 
                    'OrderTime': str(mod_order[1]['updateTime']), 
                    'Coin': mod_order[1]['symbol'], 
                    'OrderType': mod_order[1]['type'], 
                    'Side': mod_order[1]['side'], 
                    'PositionSide': mod_order[1]['positionSide'], 
                    'OrderPrice': mod_order[1]['price'], 
                    'OrderQty': mod_order[1]['origQty'], 
                    'ExecQty': mod_order[1]['executedQty'], 
                    'CummQuoteQty': mod_order[1]['cumQty'], 
                    'Status': mod_order[1]['status'],
                    'TimeInForce': mod_order[1]['timeInForce'],
                    'UserID': user['UserID'],
                    'ApiID': exist_api['ApiID'],
                    'OrderedVia': "MANUAL",
                })
                return mod_order
        except:
            raise serializers.ValidationError('Order could not be Modified')

# Cancel / Delete Particular Order
class CancelOpenOrderSerializer(serializers.Serializer):
    def func(self, validated_data):
        market = validated_data.get('market')
        exchange = validated_data.get('exchange')
        api_name = validated_data.get('api_name')
        coin = validated_data.get('coin')
        orderid = validated_data.get('orderid')

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
        exist_api = col6.find_one({'Name': api_name, 'Exchange': exchange, 'Type':'LIVE', 'Status': 'ACTIVE', 'created_by.UserID': user['UserID']}, {'_id':0})
        if not exist_api:
            raise serializers.ValidationError('Invalid api_name provided / API Inactive')
        
        if ('orderid' not in validated_data) or orderid == '':
            raise serializers.ValidationError('orderid is required and cannot be blank')
        
        if ('coin' not in validated_data) or coin == '':
            raise serializers.ValidationError('coin is required and cannot be blank')

        order = col9.find_one({'OrderID': orderid, 'Coin': coin, 'Status': 'NEW', 'UserID': user['UserID'], 'ApiID': exist_api['ApiID']}, {'_id': 0})
        
        if (not order) or (not coin):
            raise serializers.ValidationError('Order not Found')        

        if order['Coin'] != coin:
            raise serializers.ValidationError('Given Coin does not match the Order Coin')

        try:
            c = binanceFuturekey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY'])
            cancel_order = UMF_delete_order(c, x=coin, oid=order['OrderID'])
            col9.update_one({'OrderID': orderid, 'Coin': coin, 'Status': 'NEW', 'UserID': user['UserID'], 'ApiID': exist_api['ApiID']}, {'$set': {'Status': 'CANCELED'}})
            return cancel_order
        except:
            raise serializers.ValidationError('Order Already Cancelled.')
        
# Cancel / Delete All Open Orders for a given Coin
class CancelAllOpenOrderSerializer(serializers.Serializer):
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
        exist_api = col6.find_one({'Name': api_name, 'Exchange': exchange, 'Type':'LIVE', 'Status': 'ACTIVE', 'created_by.UserID': user['UserID']}, {'_id':0})
        if not exist_api:
            raise serializers.ValidationError('Invalid api_name provided / API Inactive')

        if ('coin' not in validated_data) or coin == '':
            raise serializers.ValidationError('coin is required and cannot be blank')
        
        orders = list(col9.find({'Coin': coin, 'Status': 'NEW', 'UserID': user['UserID'], 'ApiID': exist_api['ApiID']}))
        if not orders:
            raise serializers.ValidationError(f'No Open Orders Present for {coin}')
        
        try:
            c = binanceFuturekey(key=exist_api['Fields']['API_KEY'], secret=exist_api['Fields']['SECRET_KEY'])
            cancel_order = UMF_delete_all_orders(c, x=coin)
            col9.update_many({'UserID': user['UserID'], 'ApiID': exist_api['ApiID'], 'Status': 'NEW', 'Coin': coin}, {'$set': {'Status': 'CANCELED'}})
            return cancel_order
        except:
            raise serializers.ValidationError('Orders could not be Cancelled')