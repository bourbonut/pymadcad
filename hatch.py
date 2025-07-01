from madcad import *
from functools import reduce
from itertools import starmap

# wire:Wire|Web
def hatch_wire(points, edges, width: float, angle: float, normal: vec3) -> Web:
    def update(x, y):
        for key, value in y.items():
            item = x.setdefault(key, [])
            x[key] += [value]
        return x

    hatch = lambda A, B: hatch_edge(A, B, width, angle, normal)
    pairs = [(points[i], points[j]) for i, j in edges]
    d = reduce(update, starmap(hatch, pairs), {})
    return reduce(lambda x, y: x + list(zip(y, y)), map(iter, d.values()), [])


def hatch1d(start: float, end: float, width: float) -> float:
    start = (start // width + 1) * width
    while start < end:
        yield start
        start += width


def hatch_edge(A: vec3, B: vec3, width: float, angle: float, normal: vec3) -> [vec3]:
    rot = angleAxis(angle, normal) * angleAxis(anglebt(normal, Z), Z)
    w = cross(rot * X, rot * Y)
    Ap = angleAxis(pi * 0.5 - angle, w) * A
    Bp = angleAxis(pi * 0.5 - angle, w) * B
    if Bp.x - Ap.x == 0.0:
        return {}
    k = lambda x: (x - Ap.x) / (Bp.x - Ap.x)
    all_x = hatch1d(min(Ap.x, Bp.x), max(Ap.x, Bp.x), width)
    return {x: ((B - A) * k(x) + A) for x in all_x}


points = [
    (0, 5),
    (4, 2),
    (6, 4),
    (10, 2),
    (10, 8),
    (16, 6),
    (17, 13),
    (14, 12),
    (12, 20),
    (8, 18),
    (6, 20),
    (2, 17),
    (5, 14),
    (3, 10),
    (1, 12),
]
points = [vec3(*p, 0) for p in points]
edges = [(i, i + 1) for i in range(len(points) - 1)] + [(-1, 0)]

# w = Wire(points)

pairs = hatch_wire(points, edges, 0.5, radians(45), Z)
show([Wire(points).close()] + [Segment(a, b) for a, b in pairs])

# A, B = points[0], points[1]
# # A, B = O, angleAxis(radians(45), Z) * X
# (Ap, Bp), others = hatch_edge(A, B, 0.5, radians(45), Z)
# base = [Segment(O, X), Segment(O, Y), Segment(O, Z)]
# segments = [Segment(A, p) for p in others]

# a = radians(45)
# rs = [(0.5 / sin(a) * x - 12 * 0.5 / sin(a)) * X for x in range(20)]
# hatched_straight_lines = [Segment(r, (r + angleAxis(a, Z) * (8 * X))) for r in rs]
# show(base + [Segment(A, B), Segment(Ap, Bp)] + segments)
