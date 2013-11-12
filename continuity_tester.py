#!/usr/bin/env python
import sys
import time
import linuxcnc
s = linuxcnc.stat()
#print [(x, getattr(s,x)) for x in dir(s)]
print "\aDING!"
while 1:
	s.poll()
	if s.probe_val:
		 sys.stdout.write("\a")
	else:
		sys.stdout.write(".")
	sys.stdout.flush()
	time.sleep(0.01)




