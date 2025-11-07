import numpy as np
from scipy.spatial import Voronoi
import networkx as nx
import svgwrite
import bluenoise

def main():
  # Step 1: Generate random points
  # P = np.random.rand(100, 2)
  P = bluenoise.generate((1, 1), radius=0.05)

  # Tile left and right
  # shiftback = P.copy()
  # shiftforward = P.copy()
  # shiftback[:, 0] = shiftback[:, 0] - 1
  # shiftforward[:, 0] = shiftforward[:, 0] + 1
  # P = np.vstack([P, shiftback, shiftforward])

  # Tile top and bottom
  # shiftback = P.copy()
  # shiftforward = P.copy()
  # shiftback[:, 1] = shiftback[:, 1] - 1
  # shiftforward[:, 1] = shiftforward[:, 1] + 1
  # P = np.vstack([P, shiftback, shiftforward])

  # Conservative tile left and right
  shiftback = P[P[:, 0] > 0.8]
  shiftforward = P[P[:, 0] < 0.2]
  shiftback[:, 0] = shiftback[:, 0] - 1
  shiftforward[:, 0] = shiftforward[:, 0] + 1
  P = np.vstack([P, shiftback, shiftforward])

  # Conservative tile top and bottom
  shiftback = P[P[:, 1] > 0.8]
  shiftforward = P[P[:, 1] < 0.2]
  shiftback[:, 1] = shiftback[:, 1] - 1
  shiftforward[:, 1] = shiftforward[:, 1] + 1
  P = np.vstack([P, shiftback, shiftforward])

  vor = Voronoi(P)

 # Step 2: Build adjacency graph
  region_map = {}
  for i, region_index in enumerate(vor.point_region):
    region_map[i] = region_index

  G = nx.Graph()
  for (p1, p2) in vor.ridge_points:
    r1 = vor.point_region[p1]
    r2 = vor.point_region[p2]
    if -1 not in vor.regions[r1] and -1 not in vor.regions[r2]:
      G.add_edge(r1, r2)

  # Step 3: Define color palette (10 distinct colors)
  palette = ['#ff0000', '#ff7700', '#ffff00', '#77ff00', '#00ff00', '#00ff77', '#00ffff', '#0000ff', '#0077ff', '#7700ff']

  # Step 4: Color the graph using greedy coloring
  coloring = nx.coloring.equitable_color(G, num_colors=len(palette))

  # Step 5: Create SVG drawing
  dwg = svgwrite.Drawing('voronoi.svg', size=('1200px', '1200px'))
  scale = 400  # scale to fit SVG canvas if using mirroring
  # scale = 800  # scale to fit SVG canvas if not using mirroring

  # Step 6: Draw Voronoi regions
  for i, region_index in enumerate(vor.point_region):
    region = vor.regions[region_index]
    if not -1 in region and len(region) > 0:
      polygon = [vor.vertices[j] * scale + scale for j in region] # if using mirroring
      # polygon = [vor.vertices[j] * scale for j in region] # if not using mirroring
      color_index = coloring.get(region_index, 0) % len(palette)
      dwg.add(dwg.polygon(points=polygon, fill=palette[color_index], stroke='none'))

  # Step 7: Save SVG
  dwg.save()
  print("Voronoi diagram saved as 'voronoi.svg'")

if __name__ == "__main__":
    main()
