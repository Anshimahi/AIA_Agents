"GRID PAINTING"
import random
n = 7  
grid = [[random.choice([0,0,0,0,-1]) for _ in range(n)] for _ in range(n)]
grid[0][0] = grid[n-1][n-1] = 0  # Ensure free start
original = [row[:] for row in grid]  # Copy
moves = [(1,0),(-1,0),(0,1),(0,-1)]
s1, s2 = [(0,0)], [(n-1,n-1)]
grid[0][0], grid[n-1][n-1] = 1, 2
def dfs_step(stack, color):
    if not stack: 
        return
    r, c = stack[-1]  # Peek (do not pop first)
    painted = False
    for dr, dc in moves:
        nr, nc = r+dr, c+dc
        if 0<=nr<n and 0<=nc<n and grid[nr][nc] == 0:
            grid[nr][nc] = color     # Paint neighbor
            stack.append((nr,nc))    # Continue DFS deeper
            painted = True
            break  
    if not painted:
        stack.pop()
while s1 or s2:
    dfs_step(s1, 1)   # Bot1 step
    dfs_step(s2, 2)   # Bot2 step
print("\n🧱 ORIGINAL GRID (-1=blocked,0=free):")
for r in original: print(r)
print("\n🎨 PAINTED GRID (1=Bot1,2=Bot2):")
for r in grid: print(r)
