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
advantages: correct visualization in AXIS, uses saved intermediate results..
disadvantages: first moves not adjusted (when not all coordinates were used yet)..watch out..this is really just for compensating a bumpy pcb,
you must start out above it), for heavy terrain, use the HAL stuff. no support for anything beyond g0/g1, this wont adjust your drill files
comments on move lines are not preserved. this is getting beyond the sanity limits of this regex parser.

(?)use the function in scan-function.ngc to create a heights file (filename.txt probably in your config dir/home dir) (todo, edit and use scan-surface.ngc instead)
then run the script on that and your g-code file

scan-function.ngc, scan-surface.ngc
---
same things, -function should allow you to load it, then call it interactively.
both files are from https://github.com/cnc-club/linuxcnc-engraving-comp
todo add max found height to safe distance

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
a linuxcnc kinematic module, must be compiled. probably smart, but comes with a warning about a bug where coordinates fall through between triangles:-)

includes nice utilities for visualization..can be used separately:
git clone git://git.mah.priv.at/emc2-dev.git
cd emc2-dev
git checkout probekins
cd src/emc/kinematics
#if you get crap from probe2stl.py, remove odd lines (the ones that are output when probe goes down):
awk 'NR%2==0' heights.txt | ./probe2stl.py  > stl.stl
#or checkout bd5aa8f27e6ab3a0d0a4d407252d18bbc0537e4e, this old version will just output a warning
python stlvis.py stl.stl


https://github.com/cnc-club/linuxcnc-engraving-comp
-
a component too, but in python. adds some buttons into AXIS
(i have yet to make this work) (see my fork)



