from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import views
from .serializers import *

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

class AddApiView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = AddApiSerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': 'Api added Successfully !'}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: Add Api', err)
            return Response({'error': 'Error Occurred!'})