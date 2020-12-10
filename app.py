import sys, traceback, os

def exceptionHandleri(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exc(limit=2, file=sys.stdout)
    print(repr(traceback.extract_tb(exc_traceback)))
    print(exc_type, exc_value)
    print('Ja se Error: ', e)

while(True):
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

  except Exception as e:
    exceptionHandleri(e)