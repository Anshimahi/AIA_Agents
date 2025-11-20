fires = [(2, 5), (8, 1), (6, 7), (3, 9)]

firefighters = [
    ["A", 0, 0, None],
    ["B", 10, 0, None],
    ["C", 5, 10, None]
]

def manhattan(ax, ay, bx, by):
    return abs(ax - bx) + abs(ay - by)

while fires or any(f[3] for f in firefighters):
    for f in firefighters:
        name, x, y, task = f

        if task is None:
            if not fires:
                continue
            nearest = min(fires, key=lambda fire: manhattan(x, y, fire[0], fire[1]))
            f[3] = nearest
            fires.remove(nearest)

        tx, ty = f[3]

        if (x, y) != (tx, ty):
            if x < tx: x += 1
            elif x > tx: x -= 1
            if y < ty: y += 1
            elif y > ty: y -= 1
            f[1], f[2] = x, y
        else:
            print(name, "extinguished fire at", f[3])
            f[3] = None