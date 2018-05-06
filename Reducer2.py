#!/usr/bin/env python
import sys
import string

sums = 0L

for line in sys.stdin:
  line = line.strip()
  split = line.split(" ")
  response_bytes = split[0]
  sums = sums + int(response_bytes)
  
print (sums)
