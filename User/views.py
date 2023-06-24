from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import views
import Core.telegram as tg
from .serializers import *

class RegisterUserView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = RegisterUserSerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': 'User Registration Successful!'}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: User Registration', err)
            return Response({'error': 'Error Occurred!'})
        
class UserLoginView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = LoginUserSerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': 'Login Successful', 'jwt': user}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: User Login', err)
            return Response({'error': 'Error Occurred'})

class ViewProfileView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = ViewProfileSerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': user}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: View User Profile', err)
            return Response({'error': 'Error Occurred'})
        
class UpdateProfileView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = UpdateProfileSerializer()
            user = serializer.func(request.data)
            if user == 1:
                return Response({'data': "Username same as Before"}, status=200)
            if user == 2:
                return Response({'data': 'UserName Updated Successfully'}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: Update User Profile', err)
            return Response({'error': 'Error Occurred'})