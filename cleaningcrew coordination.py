import random

# ---------- GRID SETUP ----------
n = 6
grid = [[random.choice([0,1]) for _ in range(n)] for _ in range(n)]
start = {"B1":[0,0], "B2":[n-1,n-1]}
cleaned = {"B1":0, "B2":0}

initial = [row[:] for row in grid]  # copy

# ---------- A* FUNCTION (no heapq) ----------
def h(a,b): return abs(a[0]-b[0]) + abs(a[1]-b[1])
def Astar(s,g):
    openL, close, par = [tuple(s)], set(), {tuple(s):None}
    gCost, fCost = {tuple(s):0}, {tuple(s):h(s,g)}
    while openL:
        cur = min(openL, key=lambda x: fCost.get(x,1e9))
        if cur == g:
            path = []
            while cur: path.append(cur); cur = par[cur]
            return path[::-1]
        openL.remove(cur); close.add(cur)
        x,y = cur
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx,ny = x+dx,y+dy
            if 0<=nx<n and 0<=ny<n and grid[nx][ny] != -1:
                nxt=(nx,ny)
                if nxt in close: continue
                new = gCost[cur] + 1
                if nxt not in gCost or new < gCost[nxt]:
                    gCost[nxt] = new; par[nxt] = cur
                    fCost[nxt] = new + h(nxt,g)
                    if nxt not in openL: openL.append(nxt)
    return None

# ---------- MAIN CLEANING LOOP ----------
dirty = [(i,j) for i in range(n) for j in range(n) if grid[i][j]==1]
total = len(dirty)

while dirty:
    for b in ["B1","B2"]:
        if not dirty: break
        pos = tuple(start[b])
        # choose target by best A* path length
        best = min((d for d in dirty if Astar(pos,d)), key=lambda d:len(Astar(pos,d)), default=None)
        if not best: continue
        for step in Astar(pos,best)[1:]:
            start[b] = list(step)  # move bot
        x,y = best
        if grid[x][y]==1: grid[x][y] = 2 if b=="B1" else 3; cleaned[b]+=1
        dirty.remove(best)

# ---------- OUTPUT ----------
print("\nInitial grid (0 clean,1 dirty):")
for r in initial: print(r)

print("\nFinal grid (2=B1,3=B2):")
for r in grid: print(r)

eff = sum(cleaned.values())/total*100 if total>0 else 100
print("\nBot1 cleaned:",cleaned["B1"])
print("Bot2 cleaned:",cleaned["B2"])
print("Efficiency:",round(eff,2),"%")
