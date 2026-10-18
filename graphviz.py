import collections
import random

import pyvis.network as pyvisnet
import matplotlib.pyplot as plt
import networkx

RANDOM_SEED = 683061
rng = random.Random(RANDOM_SEED)

class WeightedGraph:
      def __init__(self, nodes):
        self.nodes = nodes
        self.edges = collections.defaultdict(int)
        self.adj = collections.defaultdict(set)

      def add_or_inc(self, u, v, w):
        if u == v:
          return
        a, b = (u, v) if u < v else (v, u)
        self.edges[(a, b)] += w
        self.adj[a].add(b)
        self.adj[b].add(a)

      def subgraph_by_weight(self, min_weight):
        subgraph = WeightedGraph(self.nodes)
        for (u, v), weight in self.edges.items():
          if weight >= min_weight:
            sub.add_or_inc(u, v, weight)
        return subgraph

def simulate_random_graph():
    nodes = 150
    iterations = 50
    graph = WeightedGraph(nodes)
    for _ in range(iterations):
        u, v = rng.sample(range(nodes), 2)
        graph.add_or_inc(u, v, 1)
    return graph


def render_static(graph, output_file):
    nxg = networkx.Graph()
    nxg.add_nodes_from(range(graph.nodes))
    nxg.add_edges_from([(u, v) for (u, v) in graph.edges])
    plt.figure(figsize=(8,6))
    pos = networkx.spring_layout(nxg, seed=42)
    networkx.draw_networkx_nodes(
            nxg, pos, node_size=700, node_color="skyblue")
    networkx.draw_networkx_edges(
            nxg, pos, width=2, edge_color="gray")

    plt.title("Players")
    plt.axis("off")
    plt.show()


def save_interactive_html(graph):
    net = pyvisnet.Network(notebook=False, height="500px", width="100%")

    for node_idx in range(graph.nodes):
        net.add_node(node_idx)

    for (u, v), weight in graph.edges.items():
        net.add_edge(u, v, value = weight)

    net.write_html("interactive_network.html")


graph = simulate_random_graph()
save_interactive_html(graph)
