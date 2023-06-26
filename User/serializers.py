from rest_framework import serializers
import datetime as dt
from Core.db import *
from Core.idgen import *
from Core.auth import *
import Core.telegram as tg
import hashlib

# Register New Users
class RegisterUserSerializer(serializers.Serializer):
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
        dupl_user = col1.find_one({'$or': [{'UserName': username}, {'Email': email}]}, {'_id': 0})
        if not dupl_user:
            user = col1.insert_one({
                'UserID': useridgen(),
                'UserName': username,
                'Email': email,
                'Password': hash_pass,
                'Status': 'ACTIVE',
                'created_at': dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            })
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
        
        hash_pass = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
        user = col1.find_one({'Email': email, 'Password': hash_pass}, {'_id': 0})
        if user:
            jwt = generate_user_token(userid=user['UserID'], email=user['Email'])
            return jwt
        else:
            raise serializers.ValidationError('Invalid Credentials Entered')
        
# View User Profile
class ViewProfileSerializer(serializers.Serializer):
    def func(self, validated_data):
        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")
        
        view_data = col1.find_one({'$or': [{'UserID': jwt_data['UserID']}, {'Email': jwt_data['Email']}]}, {'_id': 0, 'created_at': 0})
        if view_data:
            return view_data
        else:
            raise serializers.ValidationError("User does not not Exist")
        
# Update User Profile
class UpdateProfileSerializer(serializers.Serializer):
    def func(self, validated_data):
        username = validated_data.get('username')

        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")
        
        user = col1.find_one({'UserID': jwt_data['UserID'], 'Email': jwt_data['Email']}, {'_id': 0})
        if user:
            if (username == user['UserName']):
                return 1
            else:
                col1.update_one({'UserID': jwt_data['UserID']}, {'$set': {
                    'UserName': username if username else user['UserName'],
                    'updated_at': dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                }})
                tg.send(f"{user['UserName']} Updated username to {username}")
                return 2
        else:
            raise serializers.ValidationError('User does not Exist')
        
# Add/Create New API
class AddApiSerializer(serializers.Serializer):
    def func(self, validated_data):
        market = validated_data.get('market')
        exchange = validated_data.get('exchange')
        name = validated_data.get('name')
        fields = dict(validated_data.get('Fields'))
        balance = dict(validated_data.get('balance'))

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
        
        if ('Fields' not in validated_data) or (fields == ''):
            raise serializers.ValidationError('Fields are required and cannot be blank')
        
        requested_fields = set(exist_exchange['Fields'])
        missing_fields = requested_fields.difference(fields.keys())
        if (set(fields) != set(requested_fields)) and (missing_fields != ''):
            raise serializers.ValidationError(f"{exchange} is missing following fields: {missing_fields}")
        
        fields = {}
        for field in requested_fields:
            if (validated_data['Fields'][field] == ''):
                raise serializers.ValidationError(f'Invalid value for {field}')
            if (field in validated_data['Fields']):
                fields[field] = validated_data['Fields'][field]
            else:
                fields[field] = exist_exchange['Fields'][field]
        validated_data['Fields'] = fields

        if ('balance' not in validated_data) or (balance == ''):
            raise serializers.ValidationError('balance is required and cannot be blank')
        
        user = col1.find_one({'UserID': jwt_data['UserID']}, {'_id': 0})
        dupl_api = col6.find_one({'$or': [{'Name': name, 'created_by': user['UserName']}, {"Exchange": exchange, 'created_by': user['UserName']}]}, {'_id': 0})
        if not dupl_api:
            api = col6.insert_one({
                'ApiID': itemidgen(),
                'Name': name,
                'Fields': fields,
                'Market': market,
                'Exchange': exchange,
                'Balance': balance,
                'Status': 'ACTIVE',
                'created_at': dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                'created_by': user['UserName']
            })
            tg.send(f"{user['UserName']} added API: {name} for {exchange} exchange")
            return api
        else:
            raise serializers.ValidationError("API with same Name or same Exchange already Present")