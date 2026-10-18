import collections
import random

import pyvis.network as pyvisnet

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


def save_interactive_html(graph):
    net = pyvisnet.Network(notebook=False, height="500px", width="100%")

    for node_idx in range(graph.nodes):
        annotation=str(node_idx)
        net.add_node(node_idx, label=annotation, title=annotation)

    for (u, v), weight in graph.edges.items():
        net.add_edge(u, v, value = weight)

    net.write_html("interactive_network.html")


graph = simulate_random_graph()
save_interactive_html(graph)
