#!/usr/bin/env python
"""
hacked together from:
https://github.com/abetusk/abes_cnc_utilities/blob/master/scri.py
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


import sys,re

mmsininch = 25.4

class Compensation :
	def __init__(self) :
		self.comp = {}
		self.x_coords = []
		self.y_coords = []
		if len(sys.argv)<3:
			print >> sys.stderr, "usage: compensation.py gcode.ngc heights.txt"
			sys.exit()

		self.range_x,self.range_y, self.len_x,self.len_y = [],[], 0,0 

		self.gfile = sys.argv[1]
		self.zfile = sys.argv[2]

	#omg, somebody cut this out, my only excuse is that i am a programming flowerpot
	def print_map(self):
		print "(points read from heights file:"
		sys.stdout.write("        |")
		for x in self.x_coords :
			sys.stdout.write("{0:.4f}".format(x).center(8))
		print ""
		print "------------------------"
		for y in self.y_coords :
			sys.stdout.write("{0:.4f}".format(y).center(8)+"|")
			for x in self.x_coords :
				if self.comp[x].has_key(y):
					cell = "{0:.4f}".format(self.comp[x][y])
				else:
					cell = "ARGH"
				sys.stdout.write(cell.center(8))
			print ""
		print ")"

	def check_map(self):
		# check map integrity, map should be rectangular! 
		for x in self.x_coords :
			for y in self.y_coords :
				if not x in self.comp or not y in self.comp[x] :  
					print >> sys.stderr, "ERROR! Map should be rectangular!\nCan not find point X %s Y %s"%(x,y)
					self.print_map()
					sys.exit()

	def max(self):
		max = None
		for y in self.y_coords :
			for x in self.x_coords :
				if self.comp[x] > max:
					max = self.comp[x][y]
		return max

                                	
	def load_zfile(self) :
		f = open(self.zfile,"r")
		probe_lines = f.readlines()

		self.comp = {}
		self.x_coords = []
		self.y_coords = []
		for line in probe_lines :
			coords = [float(i) for i in line.split()]
			x,y,z = coords[0:3]
			x,y = round(x,4), round(y,4)
			if x not in self.comp :  self.comp[x] = {}
			self.comp[x][y] = z
			if not x in self.x_coords : self.x_coords.append(x)
			if not y in self.y_coords : self.y_coords.append(y)
		self.x_coords.sort()	
		self.y_coords.sort()
		self.check_map()
		self.len_x = len(self.x_coords)
		self.range_x = range(self.len_x)
		self.len_y = len(self.y_coords)
		self.range_y = range(self.len_y)
		
		#find the smallest length that two columns/rows are distant by
		self.xstep = min([(self.x_coords[x+1] - self.x_coords[x]) for x in range(len(self.x_coords)-1)])
		self.ystep = min([(self.y_coords[x+1] - self.y_coords[x]) for x in range(len(self.y_coords)-1)])

	def get_comp(self,x,y) :
	
			#clamp the point to the coords grid
			x = max(self.x_coords[0],min(self.x_coords[-1],x))
			y = max(self.y_coords[0],min(self.y_coords[-1],y))
			
			#find x2,y2, the nearest point on the grid right/down of the point
			i = 0
			while i<self.len_x :
				if self.x_coords[i]>x : break
				i+=1
			j = 0
			while j<self.len_y :
				if self.y_coords[j]>y : break
				j+=1
		
			if i==self.len_x : i -= 1 
			if j==self.len_y : j -= 1 
		
			x2=self.x_coords[i]
			y2=self.y_coords[j]
						

			#get x1,y1
			if i<self.len_x:
				x1 = self.x_coords[max(0,i-1)]
			else:
				x1 = x2	
			
			if j<self.len_y:
				y1 = self.y_coords[max(0,j-1)]
			else:
				y1 = y2	

			# now make bilinear interpolation of the points 
			if x1 != x2 :
				z1 = ((x2-x)*self.comp[x1][y1] + (x-x1)*self.comp[x2][y1])/(x2-x1)
				z2 = ((x2-x)*self.comp[x1][y2] + (x-x1)*self.comp[x2][y2])/(x2-x1)
			else:
				z1 = self.comp[x1][y1]
				z2 = self.comp[x1][y2]
			if y1 != y2 : 
				z1 = ((y2-y)*z1 + (y-y1)*z2)/(y2-y1)
				
			#print x2,y2,z1
			return z1	
	
	def parse_and_spit_gfile_uglyfunc(self):
		gf = open( self.gfile, "r" )
		x_pnt, y_pnt  = {}, {}
		cur_x=cur_y=cur_z=old_x=old_y=old_z=x=y=z = None
		unit = "dunno"
		g_mode = ""
		feed = None
		for line in gf:
			is_move = 0
			l = line.rstrip('\n')
			# skip comments
			# assumes comments encased in parens all on one line 
			#m = re.match('^\s*\(', l)
			m = re.match('^\s*(\(|;)', l)
			if m:
				print l
				continue
			
			m = re.match('^\s*[gG]\s*(0*\d*)([^\d]|$)', l)
			if m:
				tmp_mode = m.group(1)
				if re.match('^0*20$', tmp_mode):
					unit = "inch"
					conv = mmsininch
					print l
					continue
				elif re.match('^0*21$', tmp_mode):
					unit = "mm"
					conv = 1
					print l
					continue
			
			m = re.match('^\s*[gG]\s*(0*[01])[^\d](.*)', l)
			if m:
				g_mode = m.group(1)
			m = re.match('.*[xX]\s*(-?\d+(\.\d+)?)', l)
			if m:
				is_move = 1
				cur_x = float(m.group(1))*conv
			m = re.match('.*[yY]\s*(-?\d+(\.\d+)?)', l)
			if m:
				is_move = 1
				cur_y = float(m.group(1))*conv
			m = re.match('.*[zZ]\s*(-?\d+(\.\d+)?)', l)
			if m:
				is_move = 1
				cur_z = float(m.group(1))*conv
			m = re.match('.*[fF]\s*(-?\d+(\.\d+)?)', l)
			if m:
				feed = m.group(1)
			
			if is_move and (not g_mode):
				print >> sys.stderr,  "ERROR: g_mode (0/1) not detected before coordinates"
				sys.exit(0)
			if is_move and (unit == "dunno"):
				print >> sys.stderr,  "ERROR: units (g20/21) not detected before movement commands"
				sys.exit(0)
			
			if not is_move:
				print l
				continue
			
			self.split_and_interpolate(g_mode,cur_x,cur_y,cur_z,old_x,old_y,old_z,conv,feed,l)
			
			feed = None
			old_x,old_y,old_z = cur_x,cur_y,cur_z

	def split_and_interpolate(self,g_mode,x,y,z,old_x,old_y,old_z,conv,feed,l):
		
		if old_x == None or old_y == None:
			#dont worry about splitting, initial moves are offset by max() anyway
			nsteps = 1
		else:
			nsteps = int(round(0.5+max(abs(old_x-x)/self.xstep,abs(old_y-y)/self.ystep)))
			#1 or more than 1
		
		X,Y,Z=x,y,z
		
		for step in range(1, nsteps+1):
			if step == 2:
				l = "(splitting long move, xstep is "+str(self.xstep)+"+ ystep is "+str(self.ystep)+", nsteps is "+str( nsteps)+")"
			if step > 2:
				l = "(step"+str(step)+")"
			if old_x != None:
				X=old_x + (x-old_x)/nsteps*step
			if old_y != None:
				Y=old_y + (y-old_y)/nsteps*step
			if old_z != None:
				Z=old_z + (z-old_z)/nsteps*step
			self.out(g_mode,X,Y,Z,conv,feed,l)
	

	def out(self,g_mode,x,y,z,unit_conv,feed,l):
		if x != None and y != None:
			comp = self.get_comp(x,y)
		else:
			comp = self.max()
		print "g" + g_mode,\
			"f" + feed if feed != None else "",\
			"x{0:.5f}".format(x/unit_conv) if x != None else "",\
			"y{0:.5f}".format(y/unit_conv) if y != None else "",\
			"z{0:.5f}".format((z + comp)/unit_conv) if z != None else "",\
			"("+str(z/unit_conv)+"{0:+.5f}".format(comp/unit_conv,5)+")" if z != None else "",\
			";",l
			

	def run(self) :
		self.load_zfile()
		self.parse_and_spit_gfile_uglyfunc()
		self.print_map()



comp = Compensation()
comp.run()
