import yaml
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import sys

class Topo:
    def __init__(self, yaml_string):
        raw = yaml.load(yaml_string)
        self.G = nx.Graph()
        self.hops = defaultdict(list)
        self.hops_edges = defaultdict(list)
        if 'root' not in raw.iterkeys():
            print 'Graph has no root!'
            sys.exit(1)
        self.root = str(raw.pop('root'))
        self.G.add_node(self.root)
        for node in raw.iterkeys():
            self.G.add_node(str(node))

        for node, edges in raw.iteritems():
            for edge in edges:
                self.G.add_edge(str(node), str(edge))

        edges = list(nx.traversal.bfs_edges(self.G, self.root))
        for edge in edges:
            if edge[0] == self.root: # edge[1] is single-hop
                self.hops[1].append(edge[1])
                self.hops_edges[1].append(edge)
                continue
            for i in range(1, len(edges)+1): # worst case scenario
                if edge[0] in self.hops[i]:
                    self.hops[i+1].append(edge[1])
                    self.hops_edges[1+1].append(edge)
                    continue

        print self.hops


    def draw(self):
        # node attrs
        node_size=1600
        # 1-hop, 2-hop etc
        root_color = 'red'
        node_tiers = ['blue','green','yellow']
        node_color='blue'
        node_alpha=0.3
        node_text_size=12

        # edge attrs
        edge_color='black'
        edge_alpha=0.3
        edge_tickness=1
        edge_text_pos=0.3

        f = plt.figure()

        graph_pos = nx.shell_layout(self.G)
        # draw graph
        nx.draw_networkx_nodes(self.G, graph_pos, nodelist=[self.root], alpha=node_alpha, node_color=root_color)
        for hop, nodes in self.hops.iteritems():
            if len(nodes) == 0: continue
            print hop
            nx.draw_networkx_nodes(self.G, graph_pos, nodelist=nodes,
                                   alpha=node_alpha, node_color=node_tiers[hop-1])
            nx.draw_networkx_edges(self.G,graph_pos, edgelist=self.hops_edges[hop],
                                   width=edge_tickness, alpha=edge_alpha, edge_color=edge_color)
        nx.draw_networkx_labels(self.G, graph_pos,font_size=node_text_size)

        print "Drawing..."
        #f.savefig("graph.png")
        plt.show()

if __name__ == '__main__':
    filename = sys.argv[1]
    print 'Loading topology from {0}'.format(filename)
    topo = Topo(open(filename).read())
    topo.draw()
