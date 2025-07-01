from madcad import *
from madcad.gear import gearprofile, rackprofile, repeat_circular

step = pi
r = 4
z = 12
profile = repeat_circular(gearprofile(step, z), z) #.transform(translate((-z / 2 - r) * Y))
rack = rackprofile(step).transform(translate(-r * Y - pi * X))
rack = rack.flip() + rack.transform(-pi * X).flip()

steps = 80
angle = pi / (steps + 1)
h = step / (steps + 1)
transformations = (
    translate(i * h * X) * rotate(angle * i, X) for i in range(steps + 2)
)
racks = [rack.transform(t).option(color=vec3(1.0, 0.0, 0.0)) for t in transformations]
# for r in racks:
#     r.option(color=vec3(1, 0, 0))
# profiles = [profile.transform(translate(r * 0.05 * i * Z)) for i in range(20)] + [profile.transform(translate(-r * 0.05 * i * Z)) for i in range(20)]

# rotangle = atan2(step, z / 2) / (steps + 1)
rotangle = (2 * pi / z) / (steps + 1)
profiles = [profile.transform(rotate(-rotangle * i, Z)) for i in range(steps + 2)]
profiles = [p.transform(translate((-z / 2 - r) * Y)) for p in profiles]
profiles = [p.transform(rotate(angle * i, X)) for p, i in zip(profiles, range(steps + 2))]

dot = Wire(points=[0.99 * (z / 2) * Y, (z / 2) * Y])
dots = [dot.transform(rotate(-rotangle * i, Z)) for i in range(steps + 2)]
dots = [d.transform(translate((-z / 2 - r) * Y)) for d in dots]
dots = [d.transform(rotate(angle * i, X)).option(color=vec3(0.0, 0.0, 1.0)) for d, i in zip(dots, range(steps + 2))]

# profiles = [profile]
show(profiles + dots + racks)
