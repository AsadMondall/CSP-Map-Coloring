# Md. Asad Mondall_20CSE006
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

nodes = ["Barishal", "Tekerhat", "Faridpur", "Magura", "Arpara", "Khulna", "Shalikha", "Jashore", "Gopalganj", "Kalna", "Narail", "Home"]
edges = [("Barishal", "Tekerhat", 76.6), ("Tekerhat", "Faridpur", 51.1), ("Faridpur", "Magura", 51.1), ("Magura", "Arpara", 15), ("Arpara", "Home", 1.1),
        ("Khulna", "Shalikha", 67.7), ("Shalikha", "Jashore", 31.6), ("Jashore", "Arpara", 31.6), ("Shalikha", "Arpara", 9.5),("Barishal", "Khulna", 113),("Khulna", "Jashore", 60),
         ("Tekerhat", "Gopalganj", 115.4), ("Gopalganj", "Kalna", 41), ("Kalna", "Narail", 27), ("Narail", "Arpara", 45.2)]

G = nx.Graph()
G.add_nodes_from(nodes)

for edge in edges:
    G.add_edge(edge[0], edge[1], weight=edge[2])

pos = {
    "Barishal": (4, 0),
    "Tekerhat": (3, 4),
    "Faridpur": (3, 8),
    "Magura": (1, 12),
    "Arpara": (-3, 11),
    "Khulna": (-2, 1),
    "Shalikha": (-2, 8),
    "Jashore": (-4, 3),
    "Gopalganj": (2, 3),
    "Kalna": (1, 5),
    "Narail": (0, 7),
    "Home":(-3, 13)
   
}

regions = {
    "JR": ["Arpara","Shalikha","Jashore", "Arpara"],
    "KR": ["Shalikha", "Jashore", "Khulna", "Shalikha"],
    "GR": ["Barishal", "Tekerhat", "Gopalganj", "Kalna", "Narail", "Arpara", "Shalikha", "Khulna", "Barishal"],
    "FR": ["Tekerhat", "Gopalganj", "Kalna", "Narail", "Arpara", "Magura", "Faridpur", "Tekerhat"]
}

def forward_checking(graph, colors, nodes, color_map):
    for node in nodes:
        available_colors = set(colors)
        for neighbor in graph.neighbors(node):
            if neighbor in color_map:
                available_colors.discard(color_map[neighbor])
        if available_colors:
            color_map[node] = available_colors.pop()

color_map = {}
for region, nodes in regions.items():
    if region == "JR":
        forward_checking(G, ["blue", "red", "green"], nodes, color_map)
    elif region == "GR":
        forward_checking(G, ["blue", "green", "red"], nodes, color_map)
    else:
        forward_checking(G, ["green", "red", "blue"], nodes, color_map)

plt.figure(figsize=(12, 6), facecolor='lightgrey')  
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='white')
nx.draw_networkx_edges(G, pos, width=2)
nx.draw_networkx_labels(G, pos, font_size=10, font_color='black', font_family="sans-serif")

edge_labels = {(edge[0], edge[1]): str(edge[2]) for edge in edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

for region, nodes in regions.items():
    region_nodes = [pos[node] for node in nodes]
    region_colors = [color_map[node] for node in nodes]
    polygon = Polygon(region_nodes, edgecolor='black', facecolor=region_colors[0], closed=True, linewidth=2, alpha=0.5)
    plt.gca().add_patch(polygon)
    region_center = (sum(x for x, y in region_nodes) / len(region_nodes), sum(y for x, y in region_nodes) / len(region_nodes))
    plt.text(region_center[0], region_center[1], region, ha='center', va='center', fontsize=12, color='black')


plt.title("Map Visualization with specific Regions", fontsize=16, color='green')
plt.axis("off")
plt.show()
