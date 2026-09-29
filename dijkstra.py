import networkx as nx
import matplotlib.pyplot as plt

# Створення орієнтованого графа
G = nx.DiGraph()

edges = [
    ('a', 'b', 4),
    ('a', 'e', 9),
    ('b', 'e', 2),
    ('e', 'd', 4),
    ('e', 'c', 3),
    ('d', 'f', 4),
    ('c', 'f', 12),
    ('f', 'e', 1)
]

for u, v, w in edges:
    G.add_edge(u, v, weight=w)

# Точні координати вершин для відтворення структури
pos = {
    'b': (-1.0,  1.5),
    'a': ( 1.0,  1.5),
    'e': ( 0.0,  0.0),
    'd': (-1.2, -0.9),
    'c': ( 1.2, -0.9),
    'f': ( 0.0, -2.0)
}

plt.figure(figsize=(7, 7))

# Малювання вершин
nx.draw_networkx_nodes(
    G, pos,
    node_color='white',
    edgecolors='black',
    node_size=2000,
    linewidths=1.5
)

# Підписи вершин шрифтом курсивом
nx.draw_networkx_labels(
    G, pos,
    font_size=22,
    font_family='serif',
    font_weight='normal',
    font_color='black'
)

# Малювання орієнтованих ребер (стрілок)
nx.draw_networkx_edges(
    G, pos,
    arrows=True,
    arrowsize=20,
    arrowstyle='-|>',
    node_size=2000,
    edge_color='black',
    width=1.5
)

# Підписи ваг ребер
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=edge_labels,
    font_size=13,
    font_family='sans-serif',
    font_color='black',
    rotate=False
)


import math

# Список вершин та індексація
nodes = list(G.nodes)
obj = {v: i for i, v in enumerate(nodes)}
nodes_len = len(nodes)
edges_weight = dict(nx.get_edge_attributes(G, 'weight'))

# Матриця суміжності
def matrix_adj():
    matrix = [[0] * nodes_len for _ in range(nodes_len)]
    for u, v, weight in G.edges(data='weight'):
        matrix[obj[u]][obj[v]] = weight
    return matrix

matrix = matrix_adj()

# Алгоритм Дейкстри
def dijkstra(start_idx):
    def get_link_v(v, D):
        for i, weight in enumerate(D[v]):
            if weight > 0:
                yield i

    def arg_min(T, S):
        amin = -1
        m = math.inf
        for i, t in enumerate(T):
            if t < m and i not in S:
                m = t
                amin = i
        return amin

    T = [math.inf] * nodes_len
    v = obj[start_idx]
    previous = [None] * nodes_len
    S = {v}
    T[v] = 0

    while v != -1:
        for j in get_link_v(v, matrix):
            if j not in S:
                w = T[v] + matrix[v][j]
                if w < T[j]:
                    T[j] = w
                    previous[j] = v
        v = arg_min(T, S)
        if v != -1:
            S.add(v)
            
    return T, previous

# Відновлення маршруту
def get_path(start, target, previous):
    if start == target:
        return [start]

    path = []
    current = obj[target]
    while current is not None:
        path.append(nodes[current])
        if current == obj[start]:
            break
        current = previous[current]

    # Якщо цикл завершився, але до початкової вершини не дійшли — шляху немає
    if not path or path[-1] != start:
        return []

    path.reverse()
    return path

# Розрахунок
start_idx = 'a'
dd, previous = dijkstra(start_idx)


print(f"\nПокрокові маршрути від вершини '{start_idx}':")
print("=" * 75)
print(f"{'Ціль':^6} | {'Вартість':^10} | {'Покроковий ланцюг переходів':<53}")
print("-" * 75)

for i, dist in enumerate(dd):
    target = nodes[i]
    if dist == math.inf:
        print(f"{target:^6} | {'∞':^10} | Шлях відсутній")
        continue

    path = get_path(start_idx, target, previous)
    
    if len(path) == 1:
        steps_str = f"[{path[0]}] (початкова точка)"
    else:
        steps = [f"{u} -({matrix[obj[u]][obj[v]]})-> {v}" for u, v in zip(path[:-1], path[1:])]
        steps_str = " ; ".join(steps)

    print(f"{target:^6} | {dist:^10} | {steps_str:<53}")

print("=" * 75)