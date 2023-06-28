from rest_framework import serializers
from Core.db import *
from Core.idgen import *
from Core.auth import *
import Core.telegram as tg
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

