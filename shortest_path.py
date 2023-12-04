"""
Module used to compute the shortest path from location to location.
"""

import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim


class ShortestPath():
    """
    Class used to compute the shortest path from location to location using
    Dijkstra's and A*.

    Attributes:
        start_location: String representing the starting location. Can be a
            town, or street address.
        end_location: String representing the end location. Can be a town, or
            street address.
    """
    start_location = ""
    end_location = ""

    def __init__(self, input_addresses, set_radius=1500):
        """
        Attributes:
            input_addresses: A list of strings representing a list of addresses.
        """
        self.coordinate_dict = {}
        self.radius = set_radius
        self.address_to_coords(input_addresses)
        self.graph = self.create_graph(self.coordinate_dict[input_addresses[0]], self.radius)

    def create_graph(self, coords, radius=1500):
        """
        Creates a graph of the local area.

        Args:
            coords: Tuple representing the longitude, latitude coordinates of
                desired area.
            radius: An integer representing the radius of the target circle in
                meters, with the center being `coords`. Default is 1500m.

        Returns:
            An OSMnx graph object representing a graph of the desired area.
        """
        osmnx_graph = ox.graph_from_point(coords, network_type="drive", dist=radius)
        # Displays the graph using an OSMnx plot
        #* fig, ax = ox.plot_graph(G, node_color="r")
        return osmnx_graph

    def address_to_coords(self, addresses):
        """
        Converts an address to longitude and latitude.

        Args:
            addresses: List of strings representing locations. Can be towns, or street
                addresses.

        Returns:
            A tuple representing a coordinate (latitude, longitude)
        """
        # * calling the Nominatim tool and create Nominatim class
        location = Nominatim(user_agent="Geopy Library")

        if isinstance(addresses, str):
            addresses = [addresses]

        # * entering the location name
        for address in addresses:
            # print(address)
            if address in self.coordinate_dict:
                print(f"{address} found in dictionary.")
                pass
            else:
                print(f"{address} not found in dictionary.")
                get_location = location.geocode(address)
                self.coordinate_dict[address] = (get_location.latitude, get_location.longitude)

        # * printing address
        # print(get_location.address)

        # * printing latitude and longitude
        # print("Latitude = ", get_location.latitude, "\n")
        # print("Longitude = ", get_location.longitude)

        return (get_location.latitude, get_location.longitude)

    def nearest_node(self, graph, location):
        """
        Finds the nearest node to an address in an OSMnx graph object.

        Args:
            graph: An OSMnx graph object representing a graph of a select area.
            location: A string representing the geographical address of a
                specified location.

        Returns:
            Nearest node IDs or optionally a tuple where dist contains distances
            between the points and their nearest nodes
        """
        # Checks if the coordinates exist in dict, and if not, converts them.
        coords = self.check_dictionary(location)
        # ? Should an error calculation between node and location occur?
        return ox.distance.nearest_nodes(graph, coords[0], coords[1])

    def check_dictionary(self, location):
        """
        Checks if the target location is in the coordinate dictionary, and if
        not, adds it to the dictionary.

        Args:
            location: A string representing a street address.
        """
        if location in self.coordinate_dict:
            coords = self.coordinate_dict[location]
        else:
            coords = self.address_to_coords(location)
        return coords

    def d_shortest_path(self, graph, start, end):
        """
        Renders shortest path from location A to location B using Dijkstra's

        Args:

        graph: An OSMnx graph object representing a graph of the desired area.
        start: A integer representing the node ID of the start location.
        end: A integer representing the node ID of the end location.

        Returns:
            A list of node IDs representing the shortest path from the node
            closest to the starting location, to the node closest to the ending
            location, assuming that the edges of the graph are "below capacity",
            or don't have traffic.
        """
        # Computes the start and end node IDs.
        start_node = self.nearest_node(graph, start)
        end_node = self.nearest_node(graph, end)
        print(start_node)
        print(end_node)
        return ox.routing.shortest_path(graph, start_node, end_node)

    def astar_shortest_path(self, graph, start, end):
        """
        Discovers shortest path from location A to location B using A*.

        Args:

        graph: An OSMnx graph object representing a graph of the desired area.

        start: A string representing the geographical address of the start
            location.

        end: A string representing the geographical address of the end location.

        Returns:
            A list of node IDs representing the shortest path from the node
            closest to the starting location, to the node closest to the ending
            location, assuming that the edges of the graph are "below capacity",
            or don't have traffic.
        """
        # Checks if the coordinates exist in dict, and if not, converts them.
        if start in self.coordinate_dict:
            start_coords = self.coordinate_dict[start]
        else:
            start_coords = self.address_to_coords(start)

        if end in self.coordinate_dict:
            end_coords = self.coordinate_dict[end]
        else:
            end_coords = self.address_to_coords(end)

        # Computes the start and end node IDs.
        start_node = self.nearest_node(graph, start_coords)
        end_node = self.nearest_node(graph, end_coords)

        return nx.astar_path(graph, start_node, end_node, heuristic=None)