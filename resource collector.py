import math

class Agent:
    def __init__(self, x, y):   # <-- FIXED
        self.x = x
        self.y = y
        self.collected = 0

def dist(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)   # <-- FIXED

resources = [
    (1,3), (2,5), (5,1), (6,8), (9,3),
    (3,7), (8,2), (7,6), (4,4), (10,5)
]

A = Agent(2, 2)
B = Agent(8, 8)
C = Agent(10, 2)

agents = [A, B, C]

while resources:
    for ag in agents:
        if not resources:
            break
        
        best_dist = float("inf")
        best_idx = 0

        for i, (rx, ry) in enumerate(resources):
            d = dist(ag.x, ag.y, rx, ry)
            if d < best_dist:
                best_dist = d
                best_idx = i

        ag.collected += 1
        ag.x, ag.y = resources[best_idx]
        resources.pop(best_idx)

print("A collected:", A.collected)
print("B collected:", B.collected)
print("C collected:", C.collected)
