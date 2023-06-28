import asyncio, json
import websockets
from bson.objectid import ObjectId
from Core.db import *

# future_paper_orders = col9
# spot_paper_orders = col10

async def handle_websocket(websocket, path):
    print('Connection with Websocket Established on ws://localhost:7000/')
    pipeline = [{'$match': {'operationType': {'$in': ['insert', 'update', 'replace', 'delete']}}}]
    change_stream = db.watch(pipeline=pipeline)

    while True:
        try: 
            change = await asyncio.get_event_loop().run_in_executor(None, next, change_stream)
            paper_spot_order = col9.find_one({'_id': ObjectId(change['documentKey']['_id'])})
            paper_future_order = col10.find_one({'_id': ObjectId(change['documentKey']['_id'])})
            if paper_spot_order:
                order = paper_spot_order
            if paper_future_order:
                order = paper_future_order
            data = {}
            print(change)
            # Send New Order Details via Websocket
            if change['operationType'] == 'insert':
                data = change['fullDocument']
                data.pop('_id', None)

            # Send Update Order Details via Websocket
            elif change['operationType'] == 'update':    
                data.update({'OrderID': order['OrderID']})
                data.update(change['updateDescription']['updatedFields'])
            
            await websocket.send(json.dumps(data))

        except websockets.exceptions.ConnectionClosedError as e:
            print(e)
            continue

# Initialize Websocket
start_server = websockets.serve(handle_websocket, 'localhost', 7000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()