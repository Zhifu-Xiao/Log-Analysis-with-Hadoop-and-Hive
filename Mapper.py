#!/usr/bin/env python
import sys
import string

for line in sys.stdin:
  status_code = ""
  line = line.strip()
  split = line.split(" ")
  
  if (len(split) > 9):
    status_code = split[9]
	
  print(status_code)

