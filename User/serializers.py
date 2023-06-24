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
                'UserID': idgen(),
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
                tg.send(f'{username} Updated UserName')
                return 2
        else:
            raise serializers.ValidationError('User does not Exist')
        