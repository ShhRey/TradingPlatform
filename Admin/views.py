from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import views
from .serializers import *

class RegisterAdminView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = RegisterAdminSerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': 'Admin Registration Successful!'}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: Admin Registration', err)
            return Response({'error': 'Error Occurred!'})
        
class AdminLoginView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = AdminLoginSerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': 'Login Successful', 'jwt': user}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: Admin Login', err)
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
            tg.send(f'Error Occurred at \nAPI: View Admin Profile', err)
            return Response({'error': 'Error Occurred!'})

class AddMarketView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = AddMarketSerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': 'Market added Successfully !'}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: Add Market', err)
            return Response({'error': 'Error Occurred!'})

class AddExchangeView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = AddExchangeSerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': 'Exchange added Successfully !'}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: Add Exchange', err)
            return Response({'error': 'Error Occurred!'})