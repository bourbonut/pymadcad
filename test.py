# 0  1   2  3  4  5  6  7  8  9   10
# 1  0.5 0  0  0  0  0  0  0  0.5 1
# 10 5   0  0  0  0  0  0  0  5   10
# 0  5   10 10 10 10 10 10 10 5   0


def smoothstep(start, end, x):
    if x > end:
        return 1.
    elif x < start:
        return 0.
    else:
        return x / (end - start)

def apply(functions, pixels):
    result = pixels
    for f in functions:
        result = list(map(f, result))
        print(result)
    return result

# print(smoothstep(0., 5., 1))
size = 70
pixels = list(range(size + 1))
left = apply(
    [
        lambda x: 0.8 * x,
        lambda p: p % size,
        # lambda r: r * size / 2,
        # lambda r: min(r, size),
    ], pixels
)
print("=========")
right = apply(
    [
        lambda x: 0.8 * x,
        lambda p: size - p % size,
        # lambda r: r * size / 2,
        # lambda r: min(r, size),
    ], pixels
)
print("=========")
result = [min(l, r) for l, r in zip(left, right)]
print(result)
print([1. - smoothstep(0., 1., x) for x in result])
