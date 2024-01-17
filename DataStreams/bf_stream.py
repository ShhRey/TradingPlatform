from binance.um_futures import UMFutures
import websocket, json

my_api_key = ''
my_secret_key = ''

def generate_UMF_ListenKey(key, secret):
    fc = UMFutures(key=key, secret=secret)
    listen_key_info = fc.new_listen_key()
    listen_key = listen_key_info['listenKey']
    return listen_key


def on_message(ws, message):
    data = json.loads(message)
    if data['e'] == 'MARGIN_CALL':
        print('mc', data)
    if data['e'] == 'ACCOUNT_UPDATE':
        print('au', data)
    if data['e'] == 'ORDER_TRADE_UPDATE':
        print('ote', data)
    if data['e'] == 'ACCOUNT_CONFIG_UPDATE':
        print('acu', data)
    if data['e'] == 'STRATEGY_UPDATE':
        print('su', data)
    if data['e'] == 'CONDITIONAL_ORDER_TRIGGER_REJECT':
        print('cotr', data)

def on_error(ws, error):
    print('WebSocket Error:', error)

def on_close(ws):
    print('WebSocket Connection Closed')


def future_binance_stream(key, secret):
    try:
        flk = generate_UMF_ListenKey(key=key, secret=secret)
        print('Generated Listen Key: ', flk)
        url = "wss://fstream.binance.com/ws/"+flk
        ws = websocket.create_connection(url)
        print('Binance Future Payload Connection Established')
        while True:
            data = ws.recv()
            on_message(ws, data)
    except Exception as e:
        raise Exception('Error connecting Binance Stream', e)
    finally:
        ws.close()

try:
    stream = future_binance_stream(key=my_api_key, secret=my_secret_key)
except:
    raise Exception('Check Binance Credentials')
