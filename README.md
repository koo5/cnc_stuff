linuxcnc
=========

continuity_tester.py
---
a script that makes a beeping (terminal bell) continuity tester from your zprobe, prints "." or "\aBEEP" in a loop
warning: better dont leave running continuously, but only when needed. Seems to have some nasty interaction with restarting AXIS(?)

h.ini
---
my notes for linuxcnc settings file


compensation.py
---
my stab at a preprocessing z compensation
(?)use the function in scan-function.ngc to create a heights file (filename.txt probably in your home dir)
then run the script on that and your g-code file

todo: split long moves, thats where the real-timers, hal-gamers are better (well and super-sexily copying surfaces while jogging):
	xstep=self.xcoords[1] - self.xcoords[0]
	if abs(curx-oldx) > xstep or abs(cury-oldy) > ystep:
		for x=oldx;x<curx;x+=xstep...
(dont support anything beyond g0/g1 i guess)

scan-function.ngc, scan-surface.ngc
---
same things, -function should allow you to load it, then call it interactively.
both files are from https://github.com/cnc-club/linuxcnc-engraving-comp


what else is there for height compensation
===
prepending the probing g-code to yours
---
you wont see the adjusted heights in your AXIS path visualization..you will always have to do it over again..on a fresh spot..
http://wiki.linuxcnc.org/cgi-bin/wiki.pl?PCB_Milling_And_Drilling_With_Cheap_And_Simple_Height-Probing
-
the c code has been apparently rewritten to the python gui.
in both cases, a probing gcode is prepended to the start of your gcode, and has to do the probing every time, results arent saved anywhere.

realtime in HAL
---
this should let you copy the surface while jogging. again will make things look as flat though
http://wiki.linuxcnc.org/cgi-bin/wiki.pl?ProbeKins
-
a linuxcnc kinematic module, must be compiled. includes nice utilities for visualization..could be used separately, (on the linuxcnc probe output file)
converts heightmap into triangles...probably smart, but comes with a warning about a bug where coordinates fall through between triangles:-)
(i have yet to try this out)

https://github.com/cnc-club/linuxcnc-engraving-comp
-
a component too, but in python. adds some buttons into AXIS
(i have yet to make this work)




