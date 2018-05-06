#!/usr/bin/env python
import sys
import string

last_code = None
count = 0

for line in sys.stdin:
  line = line.strip()
  split = line.split(" ")
  status_code = split[0]

  if not last_code:
    last_code = status_code
    count = 1

  if status_code == last_code:
    count = count + 1

  else:
    print '%s\t%s' % (last_code, count)
    last_code = status_code
    count = 1

print '%s\t%s' % (status_code, count)
