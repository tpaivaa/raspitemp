import os
global sensortemps
sensortemps = {}
basepath = '/sys/bus/w1/devices/'
with os.scandir(basepath) as entries:
  for entry in entries:
    if entry.name.startswith('28'):
      with open(basepath + entry.name + '/w1_slave') as f:
        temp = int(f.read().split('t=')[1])
        temp = round(temp,2)
        print(entry.name + ':' + str(temp)
        sensortemps[entry.name] = temp

print(sensortemps)