from rest_framework import serializers
from Core.db import *
from Core.idgen import *
from Core.auth import *
import Core.telegram as tg
from Binance_SPOT.trade_func import *
from Binance_FUTURE.trade_func import *
import hashlib, datetime as dt

# Register New Users
class RegisterUserSerializer(serializers.Serializer):
    def func(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        confirm_password = validated_data.get('confirm_password')
        userid = useridgen()

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
        
        exchanges = list(col5.find({}, {'_id': 0, 'created_at': 0, 'created_by': 0}))
        hash_pass = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()

        pipeline = [
            {'$match': {'$or': [{'UserName': username}, {'Email': email}]}},
            {'$project': {'_id': 0}}
        ]
        
        dupl_user = list(col1.aggregate(pipeline))
        if not dupl_user:
            user = col1.insert_one({
                'UserID': userid,
                'UserName': username,
                'Email': email,
                'Password': hash_pass,
                'Status': 'ACTIVE',
                'created_at': dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            })

            bulk_insertions = [{
                'ApiID': itemidgen(), 
                'Name': exchange['Name']+'_PaperApi', 
                'Market': exchange['Market'],
                'Exchange': exchange['Name'],
                'Balance': {'USDT': '10000', 'BUSD': '10000', 'BTC': '5', 'ETH': '10', 'BNB': '100'}, 
                'Type': 'PAPER',
                'Status': 'ACTIVE',
                'created_at': dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                'created_by': {'UserID': userid, 'Name': username}
            } for exchange in exchanges]
            col10.insert_many(bulk_insertions)
            tg.send(f'{username} Registered on TradeKeen using {email}')
            return user
        else:
            raise serializers.ValidationError('User with Same Username or Email Already Exists !')
        
# Existing User Login
class LoginUserSerializer(serializers.Serializer):
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
            {'$project': {'_id': 0, 'UserID': 1, 'Email': 1}}
        ]
        user = col1.aggregate(pipeline)
        user_data = next(user, None)
        if user_data:
            jwt = generate_user_token(userid=user_data['UserID'], email=user_data['Email'])
            return jwt
        else:
            raise serializers.ValidationError('Invalid Credentials Entered')
        
# View User Profile
class ViewProfileSerializer(serializers.Serializer):
    def func(self, validated_data):
        if "jwt" not in validated_data or validated_data.get("jwt") == '':
            raise serializers.ValidationError('jwt is required and cannot be blank')
        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")
        
        pipeline = [
            {'$match': {'$or': [{'UserID': jwt_data['UserID']}, {'Email': jwt_data['Email']}]}},
            {'$project': {'_id': 0, 'created_at': 0}}
        ]
        user = col1.aggregate(pipeline)
        view_data = next(user, None)
        if view_data:
            return view_data
        else:
            raise serializers.ValidationError("User does not not Exist")
        
# Update User Profile
class UpdateProfileSerializer(serializers.Serializer):
    def func(self, validated_data):
        username = validated_data.get('username')

        if "jwt" not in validated_data or validated_data.get("jwt") == '':
            raise serializers.ValidationError('jwt is required and cannot be blank')
        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")
        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")
        
        pipeline = [
            {'$match': {'UserID': jwt_data['UserID'], 'Email': jwt_data['Email']}},
            {'$project': {'_id': 0, 'UserName': 1}}
        ]
        
        user = col1.aggregate(pipeline)
        user_data = next(user, None)
        if user_data:
            update_pipeline =[
                {'$match': {'UserID': jwt_data['UserID']}},
                {'$addFields': {
                    'UserName': {'$cond': [{'$eq': [username, None]}, '$UserName', username]},
                    'updated_at': dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                }}
            ]
            col1.update_one({'UserID': jwt_data['UserID']}, update_pipeline[1]['$addFields'])
            if username and username != user_data['UserName']:
                tg.send(f"{user['UserName']} Updated username to {username}")
            
            return 1 if username == user_data['UserName'] else 2
        else:
            raise serializers.ValidationError('User does not Exist')
        
# Add/Create New API
class AddApiSerializer(serializers.Serializer):
    def func(self, validated_data):
        market = validated_data.get('market')
        exchange = validated_data.get('exchange')
        name = validated_data.get('name')
        fields = validated_data.get('fields')

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
        
        if ('name' not in validated_data) or (name == ''):
            raise serializers.ValidationError('name is required and cannot be blank')
        
        if ('fields' not in validated_data) or (not fields):
            raise serializers.ValidationError('fields are required and cannot be blank')
        
        requested_fields = set(exist_exchange['Fields'])
        missing_fields = requested_fields.difference(fields.keys())
        if (set(fields) != set(requested_fields)) and (missing_fields != ''):
            raise serializers.ValidationError(f"{exchange} is missing following fields: {missing_fields}")
        
        fields = {}
        for field in requested_fields:
            if (validated_data['fields'][field] == ''):
                raise serializers.ValidationError(f'Invalid value for {field}')
            if (field in validated_data['fields']):
                fields[field] = validated_data['fields'][field]
            else:
                fields[field] = exist_exchange['fields'][field]
        validated_data['fields'] = fields

        try:
            if exist_exchange['Name'] == 'Binance_SPOT':
                user_client = binanceSpotkey(key=validated_data['fields']['API_KEY'], secret=validated_data['fields']['SECRET_KEY'])
                asset_bal = BS_API_Bal(c=user_client)
            if exist_exchange['Name'] == 'Binance_FUTURE':
                user_client = binanceFuturekey(key=validated_data['fields']['API_KEY'], secret=validated_data['fields']['SECRET_KEY'])
                asset_bal = UMF_API_Bal(c=user_client)
        except:
            raise serializers.ValidationError("Invalid API or SECRET KEY provided")

        user = col1.find_one({'UserID': jwt_data['UserID']}, {'_id': 0})
        pipeline = [
            {'$match': {'$or': [{'Name': name, 'created_by.Name': user['UserName']}, 
                {'Exchange': exchange, 'created_by.Name': jwt_data['UserName']},
                {'fields.API_KEY': fields.get('API_KEY', ''), 'fields.SECRET_KEY': fields.get('SECRET_KEY', '')}]
            }},
            {'$project': {'_id': 0}}
        ]
        dupl_api = list(col6.aggregate(pipeline))
        if not dupl_api:
            api = col6.insert_one({
                'ApiID': itemidgen(),
                'Name': name,
                'Fields': fields,
                'Market': market,
                'Exchange': exchange,
                'Balance': asset_bal if asset_bal else {},
                'Type': 'LIVE',
                'Status': 'ACTIVE',
                'Settings': {
                    'PositionMode': 'false',        # "true": Hedge Mode; "false": One-way Mode
                    'MultiAssetMode': 'false',      # "true": Multi-Assets Mode; "false": Single-Asset Mode
                } if exchange=='Binance_FUTURE' else {},
                'created_at': dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                'created_by': {
                    "UserID": jwt_data['UserID'],
                    "Name": user['UserName']
                }
            })
            tg.send(f"{user['UserName']} added API: {name} for {exchange} exchange")
            return api
        else:
            raise serializers.ValidationError("API with same Name+User / Exchange+User / Fields already Present")
        
# User Created Active APIs
class ActiveApiSerializer(serializers.Serializer):
    def func(self, validated_data):
        if "jwt" not in validated_data or validated_data.get("jwt") == '':
            raise serializers.ValidationError('jwt is required and cannot be blank')
        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")
        
        pipeline = [
            {'$match': {'created_by.UserID': jwt_data['UserID'], 'Type': 'LIVE', 'Status': 'ACTIVE'}},
            {'$project': {'_id': 0}}
        ]
        user_apis = list(col6.aggregate(pipeline))
        if user_apis:
            return user_apis
        else: 
            raise serializers.ValidationError('No Active APIs')