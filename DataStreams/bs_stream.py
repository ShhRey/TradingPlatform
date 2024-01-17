from binance.spot import Spot
import websocket, json

my_api_key = ''
my_secret_key = ''

def generate_BS_ListenKey(key, secret):
    fc = Spot(api_key=key, api_secret=secret)
    listen_key_info = fc.new_listen_key()
    listen_key = listen_key_info['listenKey']
    return listen_key


def on_message(ws, message):
    data = json.loads(message)
    if data['e'] == 'outboundAccountPosition':
        if data['B']:
            print('ac', data['B'])
    if data['e'] == 'balanceUpdate':
        print('bu', data)
    if data['e'] == 'executionReport':
        print('exrep', data)

def on_error(ws, error):
    print('WebSocket Error:', error)

def on_close(ws):
    print('WebSocket Connection Closed')

def spot_binance_stream(key, secret):
    try:
        slk = generate_BS_ListenKey(key=key, secret=secret)
        print('Generated Listen Key: ', slk)
        url = "wss://stream.binance.com:9443/ws/"+slk
        ws = websocket.create_connection(url)
        print("Binance Spot Payload Connection Established")
        while True:
            data = ws.recv()
            on_message(ws, data)
    except Exception as e:
        raise Exception('Error Connecting Binance Stream', e)
    finally:
        ws.close()

try:
    stream = spot_binance_stream(key=my_api_key, secret=my_secret_key)
except:
    raise Exception('Check Binance Credentials')
