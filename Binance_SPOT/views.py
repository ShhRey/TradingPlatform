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
            tg.send(f'Error Occurred at \nAPI: BinanceSpot LiveBal', err)
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
            tg.send(f'Error Occurred at \nAPI: BinanceSpot View Orders', err)
            return Response({'error': 'Error Occurred!'}) 

class OrderHistoryView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = OrderHitorySerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': user}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: BinanceSpot Order History', err)
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
            tg.send(f'Error Occurred at \nAPI: BinanceSpot Limit Buy', err)
            return Response({'error': 'Error Occurred!'})
        
class LimitSellOrderView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = PlaceLimitSellSerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': 'Order Successfully Placed.'}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: BinanceSpot Limit Sell', err)
            return Response({'error': 'Error Occurred!'})
        
class MarketBuyOrderView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = PlaceMarketBuySerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': 'Order Successfully Placed.'}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: BinanceSpot Market Buy', err)
            return Response({'error': 'Error Occurred!'})
        
class MarketSellOrderView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = PlaceMarketSellSerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': 'Order Successfully Placed.'}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: BinanceSpot Market Sell', err)
            return Response({'error': 'Error Occurred!'})

class ModifyOrderView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = ModifyOrderSerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': 'Order Modified Successfully.'}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: BinanceSpot Modify Order', err)
            return Response({'error': 'Error Occurred!'})

class CancelOpenOrderView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = CancelOpenOrderSerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': 'Order Cancelled Successfully.'}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: BinanceSpot Cancel Order', err)
            return Response({'error': 'Error Occurred!'})
        
class CancelAllOpenOrdersView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = CancelAllOpenOrderSerializer()
            user = serializer.func(request.data)
            if user:
                return Response({'data': 'Orders Cancelled Successfully.'}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: BinanceSpot Cancel All Open Order', err)
            return Response({'error': 'Error Occurred!'})