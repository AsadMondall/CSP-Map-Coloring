# Md. Asad Mondall_20CSE006
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from collections import Counter
from queue import Queue

# Define the nodes and edges
nodes = ["Barishal", "Tekerhat", "Faridpur", "Magura", "Arpara", "Khulna", "Shalikha", "Jashore", "Gopalganj", "Kalna", "Narail", "Home"]
edges = [("Barishal", "Tekerhat", 76.6), ("Tekerhat", "Faridpur", 51.1), ("Faridpur", "Magura", 51.1), ("Magura", "Arpara", 15), ("Arpara", "Home", 1.1),
        ("Khulna", "Shalikha", 67.7), ("Shalikha", "Jashore", 31.6), ("Jashore", "Arpara", 31.6), ("Shalikha", "Arpara", 9.5),("Barishal", "Khulna", 113),("Khulna", "Jashore", 60),
         ("Tekerhat", "Gopalganj", 115.4), ("Gopalganj", "Kalna", 41), ("Kalna", "Narail", 27), ("Narail", "Arpara", 45.2)]

# Create a graph
G = nx.Graph()

# Add nodes to the graph
G.add_nodes_from(nodes)

# Add edges to the graph
for edge in edges:
    G.add_edge(edge[0], edge[1], weight=edge[2])

# Define positions of nodes with padding
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

# Define regions
regions = {
    "JR": ["Arpara","Shalikha","Jashore", "Arpara"],
    "KR": ["Shalikha", "Jashore", "Khulna", "Shalikha"],
    "GR": ["Barishal", "Tekerhat", "Gopalganj", "Kalna", "Narail", "Arpara", "Shalikha", "Khulna", "Barishal"],
    "FR": ["Tekerhat", "Gopalganj", "Kalna", "Narail", "Arpara", "Magura", "Faridpur", "Tekerhat"]
}

# Backtracking algorithm to check if assigning a color to a node is safe
def is_safe(node, color, graph, color_map):
    for neighbor in graph.neighbors(node):
        if color_map.get(neighbor) == color:
            return False
    return True

# AC-3 algorithm to enforce arc consistency
def ac3(graph, domains):
    queue = Queue()
    for edge in graph.edges:
        queue.put(edge)
    while not queue.empty():
        (Xi, Xj) = queue.get()
        if revise(graph, domains, Xi, Xj):
            if len(domains[Xi]) == 0:
                return False
            for Xk in graph.neighbors(Xi):
                if Xk != Xj:
                    queue.put((Xk, Xi))
    return True

def revise(graph, domains, Xi, Xj):
    revised = False
    for color in domains[Xi]:
        if not any(is_safe(Xi, color, graph, {Xi: color, Xj: c}) for c in domains[Xj]):
            domains[Xi].remove(color)
            revised = True
    return revised

# Forward checking algorithm to color the regions
def forward_checking(graph, colors, nodes, domain, color_map):
    if len(nodes) == 0:
        return True
    node = nodes[0]
    for color in domain[node]:
        if is_safe(node, color, graph, color_map):
            color_map[node] = color
            domain_copy = domain.copy()
            for neighbor in graph.neighbors(node):
                if color in domain_copy[neighbor]:
                    domain_copy[neighbor].remove(color)
            if ac3(graph, domain_copy):
                if forward_checking(graph, colors, nodes[1:], domain_copy, color_map):
                    return True
            color_map.pop(node)
    return False

# Color the regions using forward checking
color_map = {}
domain = {node: ["red", "blue", "green"] for node in nodes}
forward_checking(G, ["red", "blue", "green"], nodes, domain, color_map)

# Draw the graph with curved layout
plt.figure(figsize=(12, 6), facecolor='lightgrey')  # Set background color and size

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='white')

# Draw edges
nx.draw_networkx_edges(G, pos, width=2)

# Draw labels with specified color
nx.draw_networkx_labels(G, pos, font_size=10, font_color='black', font_family="sans-serif")

# Add edge labels with specified color
edge_labels = {(edge[0], edge[1]): str(edge[2]) for edge in edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

# Draw regions and label in the center
for region, nodes in regions.items():
    region_nodes = [pos[node] for node in nodes]
    most_common_color = Counter([color_map.get(node, 'white') for node in nodes]).most_common(1)[0][0]
    polygon = Polygon(region_nodes, edgecolor='black', facecolor=most_common_color, closed=True, linewidth=2, alpha=0.5)
    plt.gca().add_patch(polygon)
    region_center = (sum(x for x, y in region_nodes) / len(region_nodes), sum(y for x, y in region_nodes) / len(region_nodes))
    plt.text(region_center[0], region_center[1], region, ha='center', va='center', fontsize=12, color='black')

# Set the title with bright font color
plt.title("Arc Consistency", color='blue')

# Show the graph
plt.axis("off")
plt.show()
