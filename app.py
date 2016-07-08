import random
import networkx as nx
import matplotlib.pyplot as plt

from flask import Flask, send_file
from StringIO import StringIO

app = Flask(__name__)

# random walk approach, adapted from
# https://gist.github.com/bwbaugh/4602818
def random_graph(n, e):
  import networkx as nx, random
  G, nodes, edges = nx.Graph(), range(n), set()
  unvisited_nodes, visited_nodes = set(nodes), set()

  current_node = random.sample(unvisited_nodes, 1).pop()
  unvisited_nodes.remove(current_node)
  visited_nodes.add(current_node)

  while unvisited_nodes:
    next_node = random.sample(nodes, 1).pop()
    if next_node not in visited_nodes:
      edges.add((current_node, next_node))
      unvisited_nodes.remove(next_node)
      visited_nodes.add(next_node)
    current_node = next_node

  while len(edges) < e:
    edges.add(tuple(random.sample(nodes, 2)))

  G.add_edges_from(list(edges))

  return G

def draw_graph(image):
  plt.clf()
  G = random_graph(20, 20)
  pos = nx.spring_layout(G)

  nx.draw_networkx_nodes(G, pos)
  nx.draw_networkx_edges(G, pos)
  nx.draw_networkx_labels(G, pos, font_size=10)

  plt.axis('off')
  plt.savefig(image, format='png')

@app.route('/graph.png')
def serve_image():
  image = StringIO()
  draw_graph(image)
  image.seek(0)
  return send_file(image, attachment_filename='graph.png', as_attachment=True)

@app.route('/')
def index():
  return '<img src="graph.png">'