import os

basepath = '/sys/bus/w1/devices/'
with os.scandir(basepath) as entries:
  for entry in entries:
    if entry.name.startswith('28'):
      with open(basepath + entry.name + '/w1_slave') as f:
        print(entry.name + ':' + round(f.read().split('t=')[1]),1)

