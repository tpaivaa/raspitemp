#!/usr/bin/env python3.9

import sys, traceback, os
import asyncio, websockets, json, logging

log = logging.getLogger('raspitemp')
log.setLevel(logging.INFO)


async def exceptionHandleri(e):
  print('Exceptionhandlerissa')
  exc_type, exc_value, exc_traceback = sys.exc_info()
  traceback.print_exc(limit=2, file=sys.stdout)
  log.error(repr(traceback.extract_tb(exc_traceback)))
  log.error(exc_type, exc_value)
  log.error('Ja se Error: ' + str(e))

async def consumer(message):
  print('consumer')
  print(message)

async def producer_handler(websocket, path):
  while True:
    message = await getSensorTemps()
    await websocket.send(message)

async def consumer_handler(websocket, path):
  async for message in websocket:
    await consumer(message)

async def getSensorTemps():
  #print('sensorTemps')
  try:
    basepath = '/sys/bus/w1/devices/'
    sensortemps = {}
    with os.scandir(basepath) as entries:
      
      for entry in entries:
        if entry.name.startswith('28'):
          with open(basepath + entry.name + '/w1_slave') as f:
            temp = str(round(int(f.read().split('t=')[1])/1000,2))
            sensortemps[entry.name] = temp
            # print(entry.name + ':' + str(temp))
    print(sensortemps)
    log.info(sensortemps)
    return json.dumps(sensortemps)

  except Exception as e:
    await exceptionHandleri(e)

async def raspitemp(websocket, path):
  print('raspitemp')

  consumer_task = asyncio.ensure_future(consumer_handler(websocket, path))
  producer_task = asyncio.ensure_future(producer_handler(websocket, path))
  done, pending = await asyncio.wait([consumer_task, producer_task], return_when = asyncio.FIRST_COMPLETED,)
  for task in pending:
    task.cancel()
  print(done)
  '''
  sensortemps = await getSensorTemps()
  try:
    async for message in websocket:
      print(message)
      data = json.loads(message)
      log.info(data)
      print(data)
      await websocket.send(sensortemps)
  except Exception as e:
    await exceptionHandleri(e)

  finally:
    log.info('In finally')
  '''

start_server = websockets.serve(raspitemp, "0.0.0.0", 8888)
print('raspitemp after start_server')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
