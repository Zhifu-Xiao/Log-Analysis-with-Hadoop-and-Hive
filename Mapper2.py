#!/usr/bin/env python
import sys
import string
all = string.maketrans('','')
nodigs = all.translate(all, string.digits)

for line in sys.stdin:
  response_bytes = 0L
  line = line.strip()
  split = line.split(" ")
  month = split[2]
  
  if (month != 'Jul'):
    response_bytes = 0L
	
  else:
    response_bytes = split[len(split) - 1].translate(all, nodigs)
	
  if not response_bytes:
    response_bytes = 0L
  response_bytes = int(response_bytes)
  
  print(response_bytes)
