from rest_framework import serializers
from Core.db import *
from Core.idgen import *
from Core.auth import *
import Core.telegram as tg
import hashlib, datetime as dt


# Create New Market
class AddMarketSerializer(serializers.Serializer):
    def func(self, validated_data):
        name = validated_data.get('name')

        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")

        if ('name' not in validated_data) or (name == ''):
            raise serializers.ValidationError('name is required and cannot be blank')
        
        dupl_market = col4.find({'Name': name}, {'_id': 0})
        if not dupl_market:
            col4.insert_one(({
                'Name': name,
                'Coins': {},
                'Status':'ACTIVE',
                'created_at': dt.datetime().now().strftime("%d/%m/%Y, %H:%M:%S")
            }))
        else:
            raise serializers.ValidationError('Market with same name already Exists')
    
# Create New Exchange
class AddExchangeSerializer(serializers.Serializer):
    def func(self, validated_data):
        name = validated_data.get('name')
        market = validated_data.get('market')

        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")

        if ('name' not in validated_data) or (name == ''):
            raise serializers.ValidationError('name is required and cannot be blank')
        
        dupl_exchange = col5.find({'Name': name}, {'_id': 0})


# Create New API
class AddApiSerializer(serializers.Serializer):
    def func(self, validated_data):
        name = validated_data.get('name')
        market = validated_data.get('market')
        exchange = validated_data.get('exchange')

        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")

        if ('name' not in validated_data) or (name == ''):
            raise serializers.ValidationError('name is required and cannot be blank')
        
        dupl_api = col6.find({'Name': name}, {'_id': 0})