import os

def exceptionHandleri(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exc(limit=2, file=sys.stdout)
    print(repr(traceback.extract_tb(exc_traceback)))
    print(exc_type, exc_value)
    print('Ja se Error: ', e)

try:
  basepath = '/sys/bus/w1/devices/'
  with os.scandir(basepath) as entries:
    sensortemps = {}
    for entry in entries:
      if entry.name.startswith('28'):
        with open(basepath + entry.name + '/w1_slave') as f:
          sensortemps = {}
          temp = int(f.read().split('t=')[1])
          temp = round(temp,2)
          print(entry.name + ':' + str(temp)
          sensor = entry.name
          sensortemps[sensor] = str(temp)

  print(sensortemps)

except Exception as e:
  exceptionHandleri(e)