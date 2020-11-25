import os

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