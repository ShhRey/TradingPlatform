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
                return Response({'data': user, 'msg':'PositionMode is set to One-Way Mode'}, status=200)
            if user == 'True':
                return Response({'data': user, 'msg':'PositionMode is set to Hedge Mode'}, status=200)
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
            if user == 'False':
                return Response({'data': user, 'msg':'PositionMode is set to One-Way Mode'}, status=200)
            if user == 'True':
                return Response({'data': user, 'msg':'PositionMode is set to Hedge Mode'}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: BinanceFuture Change PosiMode', err)
            return Response({'error': 'Error Occurred!'}) 

class GetAssetModeView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = GetAssetModeSerializer()
            user = serializer.func(request.data)
            if user == 'False':
                return Response({'data': user, 'msg':'AssetMode is set to Single-Asset Mode'}, status=200)
            if user == 'True':
                return Response({'data': user, 'msg':'AssetMode is set to Multi-Asset Mode'}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: BinanceFuture Get AssetMode', err)
            return Response({'error': 'Error Occurred!'})

class ChangeAssetModeView(views.APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            serializer = ChangeAssetModeSerializer()
            user = serializer.func(request.data)
            if user == 'False':
                return Response({'data': user, 'msg':'AssetMode is set to Single-Asset Mode'}, status=200)
            if user == 'True':
                return Response({'data': user, 'msg':'AssetMode is set to Multi-Asset Mode'}, status=200)
        except ValidationError as ve:
            return Response({'error': ve.detail[0]})
        except Exception as err:
            tg.send(f'Error Occurred at \nAPI: BinanceFuture Change AssetMode', err)
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
            tg.send(f'Error Occurred at \nAPI: BinanceFuture Cancel Order', err)
            return Response({'error': 'Error Occurred!'})