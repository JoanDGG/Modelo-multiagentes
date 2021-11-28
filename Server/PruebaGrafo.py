from collections import deque 
graph = {1: [2, 3],
         2: [],
         3: [4, 5, 11],
         4: [],
         5: [6, 7],
         6: [],
         7: [8],
         8: [9, 10, 16],
         9: [],
         10: [5, 11],
         11: [12, 13, 14],
         12: [],
         13: [1],
         14: [15, 22, 23, 24],
         15: [10, 16, 17],
         16: [],
         17: [18, 19],
         18: [],
         19: [20, 21, 22],
         20: [],
         21: [],
         22: [25],
         23: [],
         24: [],
         25: [26],
         26: [13, 14, 27],
         27: []}

def find_shortest_path(graph, start, end):
    dist = {start: [start]}
    q = deque([start])
    while len(q):
        at = q.popleft()
        for next in graph[at]:
            if next not in dist:
                dist[next] = dist[at]+[next]
                q.append(next)
    return dist.get(end)

print(find_shortest_path(graph, 1, 16))
print(find_shortest_path(graph, 26, 9))
print(find_shortest_path(graph, 13, 27))
