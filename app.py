#!/usr/bin/env python3

import sys, traceback, os
import asyncio, websockets, json, syslog

async def exceptionHandleri(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exc(limit=2, file=sys.stdout)
    print(repr(traceback.extract_tb(exc_traceback)))
    print(exc_type, exc_value)
    print('Ja se Error: ', e)

async def getSensorTemps():
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
    return sensortemps

  except Exception as e:
    exceptionHandleri(e)

async def raspitemp(websocket, path):
  await getSensorTemps()
  try:
    async for message in websocket:
      data = json.loads(message)
      print(data)
      syslog.syslog(data)
  except Exception as e:
    await exceptionHandleri(e)

  finally:
    syslog.syslog('In finally')

start_server = websockets.serve(raspitemp, "0.0.0.0", 8888)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
