from madcad import *
from madcad.gear import *
from math import *

# z_pinion = 10
# z_wheel = 20
# pitch_cone_angle = get_pitch_cone_angle(z_pinion, z_wheel)
#
# show([bevelgear(pi, z_wheel, pitch_cone_angle)])


show([brick(width=10)])

# z_pinion = 10
# z = z_wheel = 20
# m = 0.3
# step = pi * m
# ka = 1
# kd = 1.25
# pressure_angle = pi / 9
# pitch_cone_angle = get_pitch_cone_angle(z_pinion, z_wheel)
#
# gamma_p = pitch_cone_angle  # for convenience
# gamma_b = asin(cos(pressure_angle) * sin(gamma_p))
# cos_b, sin_b = cos(gamma_b), sin(gamma_b)
# rp = z * step / (2 * pi)
# rho1 = rp / sin(gamma_p)
# rho0 = 2 * rho1 / 3
# k = sin(gamma_p) / z
# gamma_r = gamma_p - atan2(2 * kd * k, 1)
# gamma_f = gamma_p + atan2(2 * ka * k, 1)
#
# rb = rho1 * sin(gamma_b)
# center = rho1 * cos(gamma_b) * rotate(gamma_b, Y) * X
#
# circle = web(Circle((O, Z), rb)).transform(rotatearound(pi / 2, O, Y)).transform(rho1 * cos(gamma_b) * X).transform(rotatearound(gamma_b, O, Y))
#
# show([
#     Circle((O, Z), rho1),
#     # Circle((center, normalize(center)), rb),
#     circle,
# ])

# z_pinion = 10
# z_wheel = 15
# m = 0.5
# step = pi * m
# pressure_angle = pi / 9
# pitch_cone_angle = get_pitch_cone_angle(z_pinion, z_wheel)
#
# gamma_p = pitch_cone_angle # for convenience
# rp = z_pinion * step / (2 * pi)
# rho1 = rp / sin(gamma_p)
#
# angle1tooth_pinion = 2 * pi  / z_pinion
# pinion_profile = repeat(spherical_gearprofile(z_pinion, pitch_cone_angle), z_pinion, rotatearound(angle1tooth_pinion, (O, Z)))
#
# angle1tooth_wheel = 2 * pi  / z_wheel
# wheel_profile = repeat(spherical_gearprofile(z_wheel, pi / 2 - pitch_cone_angle), z_wheel, rotatearound(angle1tooth_wheel, (O, Z)))
#
# show([pinion_profile.transform(matrix4placement(z_pinion, pi / 2)), wheel_profile])
