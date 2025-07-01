from glm import *
from math import isclose
from time import perf_counter
import random
# from rich import print
from detroit import *

random.seed(42)

def sorted_edges(edges):
    for swap_index in range(len(edges) - 1):
        ref_point = edges[swap_index][1]
        for last_index in range(swap_index + 1, len(edges)):
            edge = edges[last_index]
            if isclose(sum(edge[0] - ref_point), 0, abs_tol=1e-6):
                edges[swap_index + 1], edges[last_index] = edges[last_index], edges[swap_index + 1]
                break
            if isclose(sum(edge[1] - ref_point), 0, abs_tol=1e-6):
                edges[last_index] = (edge[1], edge[0])
                edges[swap_index + 1], edges[last_index] = edges[last_index], edges[swap_index + 1]
                break

def random_vector():
    return vec3(random.random(), random.random(), random.random())

def random_edges(n):
    edges = [random_vector() for _ in range(n)]
    return [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]

x = list(range(1, 301))
y = []

for n in x:
    rg = random_edges(n) + random_edges(n)
    random.shuffle(rg)

    st = perf_counter()
    sorted_edges(rg)
    y.append(perf_counter() - st)

data = Data.arrange([x, y])

plot = Plot.lineY(data, {"x": "x", "y": "y", "stroke": "blue"}).plot()

render(data, plot)
