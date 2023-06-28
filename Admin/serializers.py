from rest_framework import serializers
from django.core.management import call_command
from Core.db import *
from Core.idgen import *
from Core.auth import *
import Core.telegram as tg
import hashlib, datetime as dt

market_types = ['BULLISH', 'BEARISH', 'SIDEWAYS']

# Register New Admins
class RegisterAdminSerializer(serializers.Serializer):
    def func(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        confirm_password = validated_data.get('confirm_password')

        if (('username' not in validated_data) or (username == '')):
            raise serializers.ValidationError('username is required and cannot be blank')
        if (('email' not in validated_data) or (email == '')):
            raise serializers.ValidationError('email is required and cannot be blank')
        if (('password' not in validated_data) or (password == '')):
            raise serializers.ValidationError('password is required and cannot be blank')
        if (('confirm_password' not in validated_data) or (confirm_password == '')):
            raise serializers.ValidationError('confirm_password is required and cannot be blank')
        if password != confirm_password:
            raise serializers.ValidationError('password and confirm_password did not match')
        
        hash_pass = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
        dupl_user = col2.find_one({'$or': [{'UserName': username}, {'Email': email}]}, {'_id': 0})
        if not dupl_user:
            user = col2.insert_one({
                'AdminID': useridgen(),
                'UserName': username,
                'Email': email,
                'Password': hash_pass,
                'Status': 'ACTIVE',
                'created_at': dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            })
            tg.send(f'{username} Registered on TradeKeen using {email}')
            return user
        else:
            raise serializers.ValidationError('Admin with Same Username or Email Already Exists !')
        
# Existing Admin Login
class AdminLoginSerializer(serializers.Serializer):
    def func(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')

        if (('email' not in validated_data) or (email == '')):
            raise serializers.ValidationError('email is required and cannot be blank')
        if (('password' not in validated_data) or (password == '')):
            raise serializers.ValidationError('password is required and cannot be blank')
        
        hash_pass = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
        user = col2.find_one({'Email': email, 'Password': hash_pass}, {'_id': 0})
        if user:
            jwt = generate_admin_token(adminid=user['AdminID'], email=user['Email'])
            return jwt
        else:
            raise serializers.ValidationError('Invalid Credentials Entered')
        
# View Admin Profile
class ViewProfileSerializer(serializers.Serializer):
    def func(self, validated_data):
        if "jwt" not in validated_data or validated_data.get("jwt") == '':
            raise serializers.ValidationError('jwt is required and cannot be blank')
        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")
        
        view_data = col2.find_one({'$or': [{'AdminID': jwt_data['AdminID']}, {'Email': jwt_data['Email']}]}, {'_id': 0, 'created_at': 0})
        if view_data:
            return view_data
        else:
            raise serializers.ValidationError("User does not not Exist")

# Create New Market
class AddMarketSerializer(serializers.Serializer):
    def func(self, validated_data):
        name = validated_data.get('name')

        if "jwt" not in validated_data or validated_data.get("jwt") == '':
            raise serializers.ValidationError('jwt is required and cannot be blank')
        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")

        if ('name' not in validated_data) or (name == ''):
            raise serializers.ValidationError('name is required and cannot be blank')
        
        admin = col2.find_one({'AdminID': jwt_data['AdminID']}, {'_id': 0})
        dupl_market = col4.find_one({'Name': name}, {'_id': 0})
        if not dupl_market and admin:
            market = col4.insert_one({
                'MarketID': itemidgen(),
                'Name': name,
                'Coins': {},
                'Status':'ACTIVE',
                'created_at': dt.datetime.now().strftime("%d-%m-%Y, %H:%M:%S"),
                'created_by': {
                    "AdminID": jwt_data['AdminID'],
                    "Name": admin['UserName']
                }
            })
            tg.send(f"{admin['UserName']} added New Market: {name}")
            return market
        else:
            raise serializers.ValidationError('Market with same name already Exists')
    
# Create New Exchange
class AddExchangeSerializer(serializers.Serializer):
    def func(self, validated_data):
        name = validated_data.get('name')
        market = validated_data.get('market')
        fields = validated_data.get('fields')
        type = validated_data.get('type')
        insert_fields = []

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
        
        if ('name' not in validated_data) or (name == ''):
            raise serializers.ValidationError('name is required and cannot be blank')
        
        if ('fields' not in validated_data) or (not fields):
            raise serializers.ValidationError('fields are required and cannot be blank')
        
        for field in fields:
            if field != '':
                insert_fields.append(str(field).upper())
            else:
                raise serializers.ValidationError('Invalid field provided')
        fields = insert_fields

        if ('type' not in validated_data) or (type == ''):
            raise serializers.ValidationError('type is required and cannot be blank')
        
        admin = col2.find_one({'AdminID': jwt_data['AdminID']}, {'_id': 0})
        dupl_exchange = col5.find_one({'Name': name}, {'_id': 0})
        if not dupl_exchange:
            exchange = col5.insert_one({
                'ExchangeID': itemidgen(),
                'Name': name,
                'Market': market,
                'Fields': fields,
                'Type': type,
                'Status': 'ACTIVE',
                'created_at': dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                'created_by': {
                    "AdminID": jwt_data['AdminID'],
                    "Name": admin['UserName']
                }
            })
            tg.send(f"{admin['UserName']} added New Exchange: {name} for {market}")
            call_command('startapp', name)
            return exchange
        else:
            raise serializers.ValidationError('Exchange with same name already Exists')
        
# Create New Strategy
class AddStrategySerializer(serializers.Serializer):
    def func(self, validated_data):
        name = validated_data.get('name')
        alias = validated_data.get('alias')
        market = validated_data.get('market')
        market_type = validated_data.get('market_type')
        exchange = validated_data.get('exchange')
        parameters = validated_data.get('parameters')
        insert_parameters = []

        if "jwt" not in validated_data or validated_data.get("jwt") == '':
            raise serializers.ValidationError('jwt is required and cannot be blank')
        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")
        
        if ('name' not in validated_data) or (name == ''):
            raise serializers.ValidationError('name is required and cannot be blank')
        
        if alias and (alias == ''):
            raise serializers.ValidationError('alias is required and cannot be blank')
        
        if ('market' not in validated_data) or (market == ''):
            raise serializers.ValidationError('market is required and cannot be blank')
        
        exist_market = col4.find_one({'Name': market}, {'_id': 0})
        if not exist_market:
            raise serializers.ValidationError('Invalid market provided')
        
        if ('market_type' not in validated_data) or (market_type == ''):
            raise serializers.ValidationError('market_type is required and cannot be blank')
        if (market_type not in market_types):
            raise serializers.ValidationError('Invalid market_type provided')
        
        if ('exchange' not in validated_data) or (exchange == ''):
            raise serializers.ValidationError('exchange is required and cannot be blank')
        exist_exchange = col5.find_one({'Name': exchange}, {'_id': 0})
        if not exist_exchange:
            raise serializers.ValidationError('Invalid exchange provided')
        
        if ('parameters' not in validated_data) or (not parameters):
            raise serializers.ValidationError('parameters are required and cannot be blank')
        
        for parameter in parameters:
            if parameter != '':
                insert_parameters.append(str(parameter).upper())
            else:
                raise serializers.ValidationError('Invalid parameter provided')
        parameters = insert_parameters

        admin = col2.find_one({'AdminID': jwt_data['AdminID']}, {'_id': 0})
        dupl_strat = col7.find_one({'Name': name}, {'_id': 0})
        if not dupl_strat:
            strategy = col7.insert_one({
                'StrategyID': itemidgen(),
                'Name': name,
                'Alias': alias if alias else "",
                'Market': market,
                'Market_Type': market_type,
                'Exchange': exchange,
                'Parameters': parameters,
                'Status': 'ACTIVE',
                'created_at': dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                'created_by': {
                    "AdminID": jwt_data['AdminID'],
                    "Name": admin['UserName']
                }
            })
            tg.send(f"{admin['UserName']} added New Strategy: {name} in {exchange} Exchange for {market} Market")
            return strategy
        else:
            raise serializers.ValidationError('Strategy with same name already Exists')