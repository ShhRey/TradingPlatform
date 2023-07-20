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
        pipeline = [
            {'$match': {'$or': [{'UserName': username}, {'Email': email}]}},
            {'$project': {'_id': 0}}
        ]
        dupl_user = list(col2.aggregate(pipeline))
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
        
        password = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
        pipeline = [
            {'$match': {'Email': email, 'Password': password}},
            {'$project': {'_id': 0, 'AdminID': 1, 'Email': 1}}
        ] 
        user = col2.aggregate(pipeline)
        user_data = next(user, None)
        if user_data:
            jwt = generate_admin_token(adminid=user_data['AdminID'], email=user_data['Email'])
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
        
        pipeline = [
            {'$match': {'$or': [{'AdminID': jwt_data['AdminID']}, {'Email': jwt_data['Email']}]}},
            {'$project': {'_id': 0, 'created_at': 0}}
        ]
        admin = col2.aggregate(pipeline)
        view_data = next(admin, None)
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
        pipeline = [
            {'$match': {'Name': name}},
            {'$project': {'_id': 0}}
        ]
        dupl_market = list(col4.aggregate(pipeline))
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
        all_users = list(col1.find({}, {'_id': 0, 'created_at': 0}))
        pipeline = [
            {'$match': {'Name': name}},
            {'$project': {'_id': 0}}
        ]
        dupl_exchange = list(col5.aggregate(pipeline))
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
            bulk_insertions = [{
                    'ApiID': user['UserID'], 
                    'Name': name+'_PaperApi', 
                    'Market': market,
                    'Exchange': name,
                    'Balance': {'USDT': '10000', 'BUSD': '10000', 'BTC': '5', 'ETH': '10', 'BNB': '100'}, 
                    'Type': 'PAPER',
                    'Status': 'ACTIVE',
                    'created_at': dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    'created_by': {'UserID': user['UserID'], 'Name': user['UserName']}
                } for user in all_users]
            col10.insert_many(bulk_insertions)

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
        pipeline = [
            {'$match': {'Name': name}},
            {'$project': {'_id': 0}}
        ]
        dupl_strat = col7.aggregate(pipeline)
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