# Dual Drone Delivery (A* + Greedy) WITHOUT heapq
import random

# ----------------- GRID SETUP -----------------
N = 10
grid = [[0 if random.random() > 0.2 else 1 for _ in range(N)] for _ in range(N)]

D1, D2 = (0, 0), (N-1, N-1)
grid[0][0] = grid[N-1][N-1] = 0  # ensure free

# Random packages
packages = set()
while len(packages) < 6:
    r, c = random.randrange(N), random.randrange(N)
    if grid[r][c] == 0 and (r, c) not in (D1, D2):
        packages.add((r, c))

# ----------------- PRINT GRID -----------------
print("\n📌 Initial Grid (D = Drone, P = Package, # = Obstacle, . = Free)\n")
for i in range(N):
    row = ""
    for j in range(N):
        if (i, j) == D1 or (i, j) == D2:
            row += "D "
        elif (i, j) in packages:
            row += "P "
        elif grid[i][j] == 1:
            row += "# "
        else:
            row += ". "
    print(row)
print()

# ----------------- A* WITHOUT heapq -----------------
def h(a, b): return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(start, goal):
    if start == goal: return [start]
    openL = [start]
    parent = {start: None}
    g = {start: 0}
    f = {start: h(start, goal)}
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]

    while openL:
        cur = min(openL, key=lambda x: f.get(x, 999999))
        if cur == goal:
            path = []
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1]
        openL.remove(cur)
        r, c = cur
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < N and 0 <= nc < N and grid[nr][nc] == 0:
                newg = g[cur] + 1
                nxt = (nr, nc)
                if nxt not in g or newg < g[nxt]:
                    g[nxt] = newg
                    parent[nxt] = cur
                    f[nxt] = newg + h(nxt, goal)
                    if nxt not in openL: openL.append(nxt)
    return None

# ----------------- DELIVERY SIMULATION -----------------
pos = {"D1": D1, "D2": D2}
steps = {"D1": 0,  "D2": 0}
assign = {"D1": [], "D2": []}
remain = set(packages)

while remain:
    best = None
    for d in ["D1", "D2"]:
        for p in remain:
            path = astar(pos[d], p)
            if path:
                L = len(path) - 1
                if best is None or L < best[3]:
                    best = (d, p, path, L)
    if not best: break

    drone, pkg, path, L = best
    assign[drone].append(pkg)
    pos[drone] = pkg
    steps[drone] += L
    remain.remove(pkg)

# ----------------- OUTPUT -----------------
print("\n📦 Package Assignments:")
print("Drone D1 ->", assign["D1"])
print("Drone D2 ->", assign["D2"])

print("\n🚁 Delivery Steps Taken:")
print("D1 Steps:", steps["D1"])
print("D2 Steps:", steps["D2"])

print("\n⏱ Total Delivery Time (parallel execution):", max(steps["D1"], steps["D2"]))
