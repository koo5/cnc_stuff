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

