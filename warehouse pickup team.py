import pandas as pd
from scipy.optimize import linear_sum_assignment

# -------------------------------------------
# Optimized Warehouse Pickup — Hungarian Algo
# -------------------------------------------

agents = {
    "A1": (1, 1),
    "A2": (8, 8)
}

tasks = [
    {"pickup": (2, 7), "drop": (1, 1)},
    {"pickup": (7, 2), "drop": (8, 8)},
    {"pickup": (5, 5), "drop": (1, 1)},
]

# Distance function
def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

agent_names = list(agents.keys())
task_ids = list(range(len(tasks)))

# Build cost matrix
cost_matrix = []
for agent in agent_names:
    row = []
    for t in tasks:
        d_agent_to_pick = dist(agents[agent], t["pickup"])
        d_pick_to_drop = dist(t["pickup"], t["drop"])
        total_cost = d_agent_to_pick + d_pick_to_drop
        row.append(total_cost)
    cost_matrix.append(row)

# Hungarian Algorithm
agent_index, task_index = linear_sum_assignment(cost_matrix)

assignments = []
total_cost = 0

# Store results
for i in range(len(agent_index)):
    a = agent_names[agent_index[i]]
    t = task_index[i]
    cost = cost_matrix[agent_index[i]][task_index[i]]
    total_cost += cost

    assignments.append({
        "Agent": a,
        "Pickup": tasks[t]["pickup"],
        "Drop": tasks[t]["drop"],
        "Travel Distance": cost
    })

# Efficiency metric
efficiency = round(total_cost / len(tasks), 2)

# Output table
df = pd.DataFrame(assignments)
df.loc[len(df)] = ["—", "—", "—", f"Efficiency = {efficiency}"]

print(df)