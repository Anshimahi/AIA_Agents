import heapq

# -------------------------------------------------------
# A* PATHFINDING
# -------------------------------------------------------
def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(start, goal, grid):
    H, W = len(grid), len(grid[0])
    open_list = []
    heapq.heappush(open_list, (0, start))
    
    came_from = {}
    g = {start: 0}

    while open_list:
        f, current = heapq.heappop(open_list)

        if current == goal:
            return reconstruct_path(came_from, current)

        x, y = current
        # 4 directions + wait
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1), (0,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == 0:
                next_cell = (nx, ny)
                tentative_g = g[current] + 1

                if next_cell not in g or tentative_g < g[next_cell]:
                    g[next_cell] = tentative_g
                    f = tentative_g + heuristic(next_cell, goal)
                    heapq.heappush(open_list, (f, next_cell))
                    came_from[next_cell] = current

    return None


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]


# -------------------------------------------------------
# AGENT CLASS (FIXED)
# -------------------------------------------------------
class Agent:
    def __init__(self, name, start, goal, priority):
        self.name = name
        self.pos = start
        self.start = start
        self.goal = goal
        self.priority = priority
        self.path = []
        self.step = 0
        self.wait_count = 0

    def compute_path(self, grid):
        self.path = astar(self.pos, self.goal, grid)
        self.step = 0

    def next_position(self):
        if self.pos == self.goal:
            return self.pos
        if self.step + 1 < len(self.path):
            return self.path[self.step + 1]
        return self.pos

    def move(self):
        if self.step + 1 < len(self.path):
            self.step += 1
            self.pos = self.path[self.step]


# -------------------------------------------------------
# MAIN COOPERATIVE PLANNER
# -------------------------------------------------------
def cooperative_planning(grid, agentA, agentB):
    agentA.compute_path(grid)
    agentB.compute_path(grid)

    t = 0
    print("Starting Cooperative Path Planning...\n")

    while not (agentA.pos == agentA.goal and agentB.pos == agentB.goal):
        A_next = agentA.next_position()
        B_next = agentB.next_position()

        collision = False

        # Same cell conflict
        if A_next == B_next:
            collision = True

        # Swap conflict
        if A_next == agentB.pos and B_next == agentA.pos:
            collision = True

        print(f"t={t}: A->{A_next}, B->{B_next}")

        if collision:
            print("  Collision detected!")

            # Priority rule
            if agentA.priority > agentB.priority:
                print("  Agent A moves, Agent B waits")
                agentA.move()
                agentB.wait_count += 1

                # Replan if waited too long
                if agentB.wait_count >= 3:
                    print("  B replanning...")
                    agentB.compute_path(grid)
                    agentB.wait_count = 0

            else:
                print("  Agent B moves, Agent A waits")
                agentB.move()
                agentA.wait_count += 1

                if agentA.wait_count >= 3:
                    print("  A replanning...")
                    agentA.compute_path(grid)
                    agentA.wait_count = 0

        else:
            # No conflict → both move
            agentA.move()
            agentB.move()

        print(f"  Positions: A={agentA.pos}, B={agentB.pos}\n")
        t += 1


# -------------------------------------------------------
# TEST EXAMPLE
# -------------------------------------------------------
grid = [
    [0,0,0,0,0],
    [0,1,1,1,0],
    [0,0,0,1,0],
    [0,1,0,0,0],
    [0,0,0,0,0]
]

# Agent A: high priority
A = Agent("A", (0,0), (4,4), priority=1)
# Agent B: low priority
B = Agent("B", (4,0), (0,4), priority=0)

cooperative_planning(grid, A, B)
