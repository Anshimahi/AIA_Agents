import random
from collections import deque

# ------------------- GRID SETUP -------------------
n = 5  # map size
# 0 = unexplored, -1 = obstacle
grid = [[random.choice([0,0,0,0,-1]) for _ in range(n)] for _ in range(n)]

# Agent starting positions
A1 = (0,0)          # Agent 1 (left side)
A2 = (n-1,n-1)      # Agent 2 (right side)

# Make sure start cells are free
grid[0][0] = 0
grid[n-1][n-1] = 0

# to record visited cells
visited = [[0]*n for _ in range(n)]

mid = n//2  # column divider

# ------------------- VALID CELL CHECK -------------------
def valid(r,c):
    return 0<=r<n and 0<=c<n and grid[r][c] != -1

# ------------------- BFS EXPLORATION FUNCTION -------------------
def explore(start, agent_side):
    q = deque([start])
    seen = set([start])

    while q:
        r,c = q.popleft()
        visited[r][c] = 1  # mark explored

        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc = r+dr, c+dc
            if valid(nr,nc) and (nr,nc) not in seen:
                # Region rule: no overlap
                if agent_side == 1 and nc < mid:
                    seen.add((nr,nc)); q.append((nr,nc))
                if agent_side == 2 and nc >= mid:
                    seen.add((nr,nc)); q.append((nr,nc))

# ------------------- RUN BOTH AGENTS -------------------
explore(A1, 1)  # Agent 1 explores left half
explore(A2, 2)  # Agent 2 explores right half

# ------------------- EFFICIENCY SCORE -------------------
free_cells = sum(grid[i][j] != -1 for i in range(n) for j in range(n))
explored = sum(visited[i][j] == 1 for i in range(n) for j in range(n))
efficiency = (explored/free_cells)*100

# ------------------- OUTPUT -------------------
print("\n🗺️ Map (-1 = obstacle, 0 = free):")
for row in grid: print(row)

print("\n🤖 Explored Cells (1 = explored, 0 = not visited):")
for row in visited: print(row)

print("\n📌 Exploration Summary:")
print("Total free cells  :", free_cells)
print("Explored cells    :", explored)
print("Exploration Efficiency:", round(efficiency,2), "%")
