import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim
from shapely.geometry import Point
import geopandas as gpd
from shortest_path import ShortestPath

address_list = ["1000 Olin Way, Needham, MA", "958 Highland Ave, Needham, MA", "Medford, MA"]
alg = ShortestPath(address_list, 5000)
# print(alg.coordinate_dict)
olin = address_list[0]
tjs = address_list[1]
medford = address_list[2]
print(alg.coordinate_dict[medford])
print(alg.coordinate_dict[olin])
print(alg.coordinate_dict[tjs])

print(alg.nearest_node(olin))
print(alg.nearest_node(tjs))
print(alg.nearest_node(medford))

shortest_path_list = alg.d_shortest_path(address_list[0], address_list[1])
print(shortest_path_list)

max_flow, flowDict = alg.max_flow_path(address_list[0], address_list[1])
path = {
    (u, v): {"actual_flow": flowDict[u][v]}
    for u in flowDict
    for v in flowDict[u]
    if flowDict[u][v] > 0
}
nx.set_edge_attributes(alg.graph, path)
print(alg.graph[1477][1476]["actual_flow"])
# nc = ["y" if () else "r" for node in alg.graph.nodes()]
# fig, ax = ox.plot_graph(alg.graph, node_color="r")
