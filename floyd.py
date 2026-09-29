import math
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

# Координати вершин
pos = {
    'b': (-1.0,  1.5),
    'a': ( 1.0,  1.5),
    'e': ( 0.0,  0.0),
    'd': (-1.2, -0.9),
    'c': ( 1.2, -0.9),
    'f': ( 0.0, -2.0)
}

plt.figure(figsize=(7, 7))

# 1. Візуалізація
nx.draw_networkx_nodes(
    G, pos,
    node_color='white',
    edgecolors='black',
    node_size=2000,
    linewidths=1.5
)

nx.draw_networkx_labels(
    G, pos,
    font_size=20,
    font_family='serif',
    font_weight='normal',
    font_color='black'
)

nx.draw_networkx_edges(
    G, pos,
    arrows=True,
    arrowsize=20,
    arrowstyle='-|>',
    node_size=2000,
    edge_color='black',
    width=1.5
)

# Додано малювання числових ваг ребер
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)

# 2. Формування матриці суміжності
nodes = list(G.nodes)
nodes_len = len(nodes)
obj = {v: i for i, v in enumerate(nodes)}

def build_initial_matrix():
    matrix = [[math.inf] * nodes_len for _ in range(nodes_len)]
    for i in range(nodes_len):
        matrix[i][i] = 0

    for u, v, weight in G.edges(data='weight'):
        matrix[obj[u]][obj[v]] = weight

    return matrix

initial_matrix = build_initial_matrix()

# 3. Алгоритм Флойда–Уоршелла
def floyd_warshall(matrix):
    dist = [row[:] for row in matrix]
    previous = [[None] * nodes_len for _ in range(nodes_len)]

    for k in range(nodes_len):
        for i in range(nodes_len):
            for j in range(nodes_len):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    previous[i][j] = k

    return dist, previous

dist_matrix, previous = floyd_warshall(initial_matrix)

# 4. Рекурсивне відновлення маршруту
def get_floyd_path(start, target, previous, dist_matrix):
    if dist_matrix[start][target] == math.inf:
        return []

    if start == target:
        return [nodes[start]]

    middle = previous[start][target]
    if middle is None:
        return [nodes[start], nodes[target]]

    left = get_floyd_path(start, middle, previous, dist_matrix)
    right = get_floyd_path(middle, target, previous, dist_matrix)

    return left[:-1] + right

# 5. Вивід результатів
for start_node in nodes:
    start_i = obj[start_node]
    print(f"Покрокові маршрути від вершини '{start_node}':\n")

    for target_i, target_node in enumerate(nodes):
        dist = dist_matrix[start_i][target_i]

        if dist == math.inf:
            print(f"• До {target_node}: шлях відсутній")
            continue

        path = get_floyd_path(start_i, target_i, previous, dist_matrix)

        if len(path) == 1:
            print(f"• До {target_node}: вартість = {dist} (початкова точка)")
        else:
            steps = [f"{u} -({initial_matrix[obj[u]][obj[v]]})-> {v}" for u, v in zip(path[:-1], path[1:])]
            print(f"• До {target_node} (довжина: {dist}):")
            print(f"  Повний ланцюг: {' ; '.join(steps)}")

    print("\n" + "=" * 50 + "\n")