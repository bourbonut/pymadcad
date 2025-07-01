from madcad import *
from operator import sub

def point_plane(plane):
    point, normal = plane
    if normal.z != 0:
        M = vec3(1, 1, point.z + (point.x * normal.x + point.y * normal.y) / normal.z)
        if M != point:
            return M
    if normal.y != 0:
        M = vec3(1, point.y + (point.x * normal.x + point.z * normal.z) / normal.y, 1)
        if M != point:
            return M
    if normal.x != 0:
        M = vec3(point.x + (point.z * normal.z + point.y * normal.y) / normal.x, 1, 1)
        if M != point:
            return M
    else:
        raise ValueError("The normal of the plane is null.")

def intersection_LP(line, plane):
    P, M1P, M2P = plane
    A, B = line
    AB = B - A
    matrix = mat3(AB, M1P, M2P)
    if determinant(matrix) == 0: # coplanar
        return None
    k, _, _ = matrix * (P - A)
    if 0 < k <= 1: # intersection
        return A + k * AB
    return None


def intersection_TP(triangle, plane):
    A, B, C = triangle
    P, _ = plane
    M = point_plane(plane)
    M1P = P - M
    M2P = cross(normal, M1P)
    S1 = intersection_LP((A, B), (P, M1P, M2P))
    S2 = intersection_LP((A, C), (P, M1P, M2P))
    S3 = intersection_LP((B, C), (P, M1P, M2P))
    return S1, S2, S3


def rasterization2D(triangle, plane):
    A, B, C = triangle
    P, normal = plane
    M = point_plane(plane)
    PM1 = M - P
    PM2 = cross(normal, PM1)
    # projection triangle to plane base
    proj = mat3(PM1, PM2, normal)
    print(A)
    print(B)
    print(C)
    print(proj)
    A = proj * A
    B = proj * B
    C = proj * C
    edges = [(A, B), (B, C), (C, A)]
    longest_edge = max(edges, key=lambda e: abs(sub(*e)).x)
    return longest_edge, list(map(lambda e: abs(sub(*e)).x, edges)), edges


# wire_section = Wire([X, 2 * X, 2 * X + Z, X + Z]).close().segmented().flip()
# washer = revolution(2 * pi, (O, Z), wire_section)
# show([washer])

A, B, C = vec3(0, 0, 0), vec3(1, 0, 0), vec3(0, 1, 0)
P = vec3(0.5, 0, -1)
normal = vec3(1, 0, 0)
# print(intersection_TP((A, B, C), (P, normal)))
print(rasterization2D((A, B, C), (P, normal)))
