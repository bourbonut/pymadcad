from madcad import *
from madcad import gear

settings.resolution = ('rad', 0.05)

axis = (vec3(0),vec3(0,0,1))

z = 8
step = 1
alpha = radians(20)
h = 0.5 * 2.25 * step/pi * cos(alpha)/cos(radians(20))
e = 0.5*h
p = step*z / (2*pi)
prof = gear.gearprofile(step, z, h, e, alpha)

show([
	vec3(0),
	vec3(1,0,0),
	(vec3(p,0,0), vec3(1,0,0)),
	
	web(prof) + web(prof).transform(angleAxis(2*pi/z, vec3(0,0,1))),
	
	Circle(axis, p),
	Circle(axis, p * cos(alpha)),
	Circle(axis, p +h +e),
	Circle(axis, p -h +e),
	], {'display_points':True})
