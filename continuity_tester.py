#!/usr/bin/env python
import sys
import time
import linuxcnc
s = linuxcnc.stat()
while 1:
	s.poll()
	if s.probe_val:
		 sys.stdout.write("\aBEEP")
	else:
		sys.stdout.write(".")
	sys.stdout.flush()
	time.sleep(0.01)




