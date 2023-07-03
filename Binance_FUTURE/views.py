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
            tg.send(f'Error Occurred at \nAPI: BinanceFuture LiveBal', err)
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
            tg.send(f'Error Occurred at \nAPI: BinanceFuture GetBal', err)
            return Response({'error': 'Error Occurred!'})

class GetPositionModeView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = GetPositionModeSerializer()
            user = serializer.func(request.data)
            if user == 'False':
                return Response({'data': user, 'msg':'PositionMode is set to One-Way Mode'})
            if user == 'True':
                return Response({'data': user, 'msg':'PositionMode is set to Hedge Mode'})
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: Get BinanceFuture PositionMode', err)
            return Response({'error': 'Error Occurred!'})

class ChangePositionModeView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = ChangePositionModeSerializer()
            user = serializer.func(request.data)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: BinanceFuture View Orders', err)
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
            tg.send(f'Error Occurred at \nAPI: BinanceFuture View Orders', err)
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
            tg.send(f'Error Occurred at \nAPI: BinanceFuture Order History', err)
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
            tg.send(f'Error Occurred at \nAPI: BinanceFuture Limit Buy', err)
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
            tg.send(f'Error Occurred at \nAPI: BinanceFuture Limit Sell', err)
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
            tg.send(f'Error Occurred at \nAPI: BinanceFuture Market Buy', err)
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
            tg.send(f'Error Occurred at \nAPI: BinanceFuture Market Sell', err)
            return Response({'error': 'Error Occurred!'})