from madcad import *
# Create a section
points = [O, X, X + Z, 2 * X + Z, 2 * (X + Z), X + 2 * Z, X + 5 * Z, 5 * Z]
section = Wire(points).segmented().flip()
# Create a revolution of `section` with the angle `2 * pi` around the axis `(O, Z)`
rev = revolution(2 * pi, (O, Z), section)
rev.mergeclose()
show([rev])
