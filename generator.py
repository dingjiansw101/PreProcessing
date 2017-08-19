
def triangles():
    a = [1]
    yield a
    for i in range(9):
        a.insert(0, 0)
        a.append(0)
        tmp = []
        for i in range(len(a) - 1):
            tmp.append(a[i] + a[i + 1])
        a = tmp
        yield a
n = 0
for t in triangles():
    print(t)
    n = n + 1
    if n == 10:
        break