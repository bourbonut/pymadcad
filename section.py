from madcad import *
from madcad.mesh.container import edgekey, suites
from madcad.hashing import PointSet
from madcad.mathutils import noproject
from madcad.gear import *
from madcad.triangulation import triangulation
from itertools import tee, compress
from functools import reduce
from operator import iadd, not_
from math import isclose, pi
from time import perf_counter
from rich import print

from madcad.rendering import drawing

# box_segments {{{
# def box_segments(mesh):
#     mi, ma = mesh.box()
#     mi *= 1.1
#     ma *= 1.1
#     a = vec3(ma.x, mi.y, mi.z)
#     b = vec3(mi.x, ma.y, mi.z)
#     c = vec3(mi.x, mi.y, ma.z)
#     d = vec3(ma.x, ma.y, mi.z)
#     e = vec3(mi.x, ma.y, ma.z)
#     f = vec3(ma.x, mi.y, ma.z)
#     segments = [
#         Segment(mi, a),
#         Segment(mi, b),
#         Segment(mi, c),
#         Segment(ma, d),
#         Segment(ma, e),
#         Segment(ma, f),
#         Segment(a, d),
#         Segment(b, e),
#         Segment(c, f),
#         Segment(a, f),
#         Segment(b, d),
#         Segment(c, e),
#     ]
#     return segments
# }}}

def seperate(mesh, plane):
    q, n = plane
    mesh_points = list(mesh.points)
    upper_faces = []
    tracks = []
    intersected_points = []

    found_points = PointSet(mesh.precision(), manage=mesh.points)

    def is_intersected(quotient, divisor):
        return divisor and 0 < quotient / divisor < 1

    def intersection_tp(face, check_is_upper):
        """Intersection betwenn a triangle and a plane"""
        a, b, c = pts = mesh.facepoints(face)
        dirs = (b - a, c - b, a - c)

        quot = transpose(mat3(q - a, q - b, q - c)) * n
        div = transpose(mat3(*dirs)) * n

        iterator = zip(pts, dirs, quot, div)
        i1, i2 = (
            point + q / d * direction
            for (point, direction, q, d) in iterator
            if is_intersected(q, d)
        )

        # Order intersected points
        two_pts = sum(check_is_upper) == 2
        conditions = map(not_, check_is_upper) if two_pts else check_is_upper
        p0 = next(compress(pts, conditions))
        tn = normalize(cross(i1 - p0, i2 - p0))
        normal = mesh.facenormal(face)
        clockwise = dot(tn, normal) > 0
        # return (i1, i2) if dot(tn, normal) > 0 else (i2, i1)
        if two_pts and clockwise:
            return (i1, i2)
        elif two_pts and not clockwise:
            return (i2, i1)
        elif not two_pts and clockwise:
            return (i2, i1)
        else:
            return (i1, i2)

        # condition = dot(cross(cross(b - a, c - a), i2 - i1), normal) > 0
        # return (i1, i2) if dot(tn, normal) > 0 else (i2, i1)

    def add_remaining_faces(face, track, check_is_upper, intersected_points):
        if check_is_upper[2] and check_is_upper[0]:
            remaining_points = (face[2], face[0])
        else:
            remaining_points = tuple(compress(face, check_is_upper))

        npoints = len(mesh_points)
        pi1, pi2 = intersected_points
        conditions = (
            map(not_, check_is_upper)
            if sum(check_is_upper) == 2
            else check_is_upper
        )
        pts = mesh.facepoints(face)
        p0 = next(compress(pts, conditions))
        tn = normalize(cross(pi1 - p0, pi2 - p0))
        normal = mesh.facenormal(face)
        pi1, pi2 = (pi1, pi2) if dot(tn, normal) > 0 else (pi2, pi1)

        i = 0
        if pi1 in found_points:
            i1 = found_points[pi1]
        else:
            i1 = found_points.add(pi1)
            mesh_points.append(pi1)

        if pi2 in found_points:
            i2 = found_points[pi2]
        else:
            i2 = found_points.add(pi2)
            mesh_points.append(pi2)

        if len(remaining_points) == 2:
            b, c = remaining_points
            pb, pc = mesh.points[b], mesh.points[c]
            ref = mesh.facenormal(face)
            upper_faces.extend((uvec3(i2, i1, b), uvec3(i2, b, c)))
            tracks.extend([track, track])
        else:
            a = remaining_points[0]
            pa = mesh.points[a]
            pi1, pi2 = intersected_points
            upper_faces.append(uvec3(a, i1, i2))
            tracks.append(track)

    for track, face in zip(mesh.tracks, mesh.faces):
        a, b, c = mesh.facepoints(face)
        vec = transpose(mat3(a - q, b - q, c - q)) * n
        check_is_upper = tuple(vec > vec3(0))
        if all(check_is_upper):
            tn = mesh.facenormal(face)
            if 2 * anglebt(n, tn) > pi:
                upper_faces.append(face)
                tracks.append(track)
        elif any(check_is_upper):
            points = intersection_tp(face, check_is_upper)
            add_remaining_faces(face, track, check_is_upper, points)
            intersected_points.append(points)
    return mesh_points, upper_faces, tracks, intersected_points

# project_pp {{{
def project_pp(mesh, plane):
    """Project edge points on plane"""
    q, n = plane
    def wrapper(edge):
        a = mesh.points[edge[0]]
        b = mesh.points[edge[1]]
        return a - dot(a - q, n) * n, b - dot(b - q, n) * n
    return wrapper
# }}}

# pairwise {{{
def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return list(zip(a, b))
# }}}

# remove_straight_points {{{
def remove_straight_points(web, plane):
    q, n = plane

    loops = suites(web.edges)
    edges = reduce(iadd, map(pairwise, loops))
    new_edges = [edges[0]]
    track = 0
    tracks = [0]
    track_indices = [0]
    for edge in edges[1:]:
        p1, p2 = web.edgepoints(new_edges[-1])
        p3, p4 = web.edgepoints(edge)
        if not isclose(l1Norm(p2 - p3), 0, abs_tol=1e-6):
            new_edges.append(edge)
            track += 1
            tracks.append(track)
            track_indices.append(len(new_edges) - 1)
        elif isclose(l1Norm(noproject(p1 - p2, p4 - p3)), 0, abs_tol=1e-6):
            old_edge = new_edges.pop()
            new_edges.append((old_edge[0], edge[1]))
        else:
            new_edges.append(edge)
            tracks.append(track)

    p1, p2 = web.edgepoints(new_edges[0])
    p3, p4 = web.edgepoints(new_edges[-1])
    same_point = isclose(l1Norm(p2 - p3), 0, abs_tol=1e-6)
    is_straight_line = isclose(l1Norm(noproject(p1 - p2, p4 - p3)), 0, abs_tol=1e-6)
    if same_point and straight_line:
        begin = new_edges.pop(0)
        end = new_edges.pop()
        new_edges.append((end[0], begin[1]))
        tracks.append(0)

    # for i, start in enumerate(track_indices):
    #     if i == len(track_indices) - 1:
    #         end = len(new_edges)
    #     else:
    #         end = track_indices[i + 1]
    #     print("=" * 10)
    #     for i1, i2 in pairwise(list(range(start, end)) + [start]):
    #         edge1 = new_edges[i1]
    #         edge2 = new_edges[i2]
    #         p1, p2 = web.edgepoints(edge1)
    #         p3, p4 = web.edgepoints(edge2)
    #         print(dot(n, normalize(cross(p2 - p1, p4 - p3))) > 0)

    return Web(points=web.points, edges=new_edges, tracks=tracks)
# }}}

def section(mesh, plane):
    st = perf_counter()
    mesh_points, upper_faces, tracks, intersected_points = seperate(mesh, plane)
    unfinished_cut = Web(
        points=reduce(iadd, intersected_points, []),
        edges=[(2 * i, 2 * i + 1) for i in range(len(intersected_points))]
    )
    unfinished_cut.mergeclose()
    cut = remove_straight_points(unfinished_cut, plane)
    cut.strippoints()
    upper_mesh = Mesh(points=mesh_points, faces=upper_faces, tracks=tracks)
    end = perf_counter()
    print(end - st)
    q, n = plane
    transformation = rotatearound(anglebt(Z, n), q, cross(Z, n)) * mat4(angleAxis(pi * 0.5, X))
    return [cut.transform(transformation), upper_mesh.transform(transformation)]
    # return [cut.transform(transformation)]


wire_section = Wire([X, 2 * X, 2 * X + Z, X + Z]).close().segmented().flip()
inside_section = web(Circle((1.5 * X + 0.5 * Z, -Y), 0.25))
washer = revolution(2 * pi, (O, Z), web(wire_section) + inside_section)
# box_segments(washer)
pitch_angle = get_pitch_cone_angle(18, 30)
g = bevelgear(1.2, 20, pitch_angle)
# s = section(g, (O, X))
# s = section(washer, (O, X))

# cut = s[0]
# edges = {track: [] for track in range(len(cut.groups))}
# for i, track in enumerate(cut.tracks):
#     edges[track].append(cut.edges[i])
# meshs = [triangulation(Web(cut.points, loop)) for loop in edges.values()]
# for i, mesh in enumerate(meshs):
#     if dot(mesh.facenormal(mesh.faces[0]), X) > 0:
#         meshs[i] = mesh.flip()
# show(meshs + [s[1]])
# show([washer])
# show(s + [mat3(X, Y, Z)])
# show([s[0]])
# show([triangulation(s[0])], options={"display_wire": True})
drawing([g], (O, X))
# print(section(washer, (O, Y)))
