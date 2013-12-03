#!/usr/bin/env python
"""
hacked together from:
https://github.com/abetusk/abes_cnc_utilities/blob/master/scri.py
(license missing)
and:
https://github.com/cnc-club/linuxcnc-engraving-comp/blob/master/compensation.py
(Copyright (C) 2009 Nick Drobchenko, nick@cnc-club.ru)
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""


import sys
from compensation import Compensation


if len(sys.argv)<3:
	print >> sys.stderr, "usage: compensation.py gcode.ngc heights.txt"
	sys.exit()


comp = Compensation(sys.argv[1], sys.argv[2])
comp.run()

