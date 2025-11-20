# Rescue Bot Squad (Concise + Fixed)

from collections import deque
import random

# Print grid
def show(g): 
    for r in g: print(" ".join(r))
    print()

# BFS shortest distance (FIXED)
def bfs_dist(maze, s, g):
    if s == g: return 0
    R,C=len(maze),len(maze[0])
    q,vis=deque([(s,0)]),{s}
    while q:
        (r,c),d=q.popleft()
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc=r+dr,c+dc
            if 0<=nr<R and 0<=nc<C and maze[nr][nc]!=1 and (nr,nc) not in vis:
                if (nr,nc)==g: return d+1
                vis.add((nr,nc)); q.append(((nr,nc),d+1))
    return float('inf')

# Simple straight movement
def go(s,g):
    (r,c),(gr,gc)=s,g; p=[]
    while r!=gr: r+=1 if r<gr else -1; p.append((r,c))
    while c!=gc: c+=1 if c<gc else -1; p.append((r,c))
    return p

def rescue(rows=10, cols=10, keys=6):
    # Build maze + random walls
    maze=[[0 if random.random()>0.12 else 1 for _ in range(cols)] for _ in range(rows)]
    A,B=(0,0),(rows-1,cols-1); maze[0][0]=maze[rows-1][cols-1]=0

    # Place victims
    V=set()
    while len(V)<keys:
        r,c=random.randrange(rows),random.randrange(cols)
        if maze[r][c]==0 and (r,c) not in (A,B): V.add((r,c))

    # Display
    disp=[['#' if maze[i][j]==1 else '.' for j in range(cols)] for i in range(rows)]
    for r,c in V: disp[r][c]='V'
    disp[0][0],disp[rows-1][cols-1]='A','B'
    print("\nInitial Maze:"); show(disp)

    # Assign closest (BFS)
    assign={v : ('A' if bfs_dist(maze,A,v)<=bfs_dist(maze,B,v) else 'B') for v in V}
    print("Assignments:",assign,"\n")

    # Rescue phase
    resA,resB=[],[]
    for v,a in assign.items():
        if a=='A': go(A,v); A=v; resA.append(v)
        else: go(B,v); B=v; resB.append(v)

    print("Rescued by A:",resA)
    print("Rescued by B:",resB)

rescue()
