from rest_framework import serializers
from Core.db import *
from Core.idgen import *
from Core.auth import *
import Core.telegram as tg

# Fetch User Balance
class FetchApiBalance(serializers.Serializer):
    def func(self, validated_data):
        if "jwt" not in validated_data or validated_data.get("jwt") == '':
            raise serializers.ValidationError('jwt is required and cannot be blank')
        try:
            jwt_data = validate_jwt(validated_data.get("jwt"))
        except:
            raise serializers.ValidationError("Invalid JWT token")