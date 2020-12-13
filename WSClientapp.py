import asyncio
import websockets, json

async def hello():
  while True:
    try:
      uri = "ws://10.10.10.6:8888"
      async with websockets.connect(uri) as websocket:
        while True:
          try:
            async for message in websocket:
              await websocket.ping()
              await websocket.pong()
              data = json.loads(message)
              print(data)
          except asyncio.TimeoutError:
            print('timeout')
            break
    except Exception as e:
      print(str(e))

asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()