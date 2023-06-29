from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import views
from .serializers import *

class LiveApiBalView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = GetLiveApiBalSerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': user}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: BinanceSpot GetBal', err)
            return Response({'error': 'Error Occurred!'})
        
class DBApiBalView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = GetDBApiBalSerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': user}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: BinanceSpot GetBal', err)
            return Response({'error': 'Error Occurred!'})
        
class OpenOrderView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = ViewOpenOrderSerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': user}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: Spot View Orders', err)
            return Response({'error': 'Error Occurred!'})
            
        
class LimitBuyOrderView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = PlaceLimitBuySerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': 'Order Successfully Placed.'}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: Spot Limit Buy', err)
            return Response({'error': 'Error Occurred!'})