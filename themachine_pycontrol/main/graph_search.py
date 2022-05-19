import pkg_resources
import pickle
import networkx as nx
from typing import Dict, List, Tuple

GRAPH_JSON = pkg_resources.resource_filename(
    "themachine_pycontrol", "graphgen/graph.json"
)



class GraphSearch:
    """
    Class that contains the functions for searching the graph representing the Machine.
    === Public Attributes ==
    graph: the graph object that search operations will be performed on
    """

    def __init__(self, graph):
        """
        Instantiates a GraphSearch object for a graph
        """
        self.graph: nx.DiGraph = graph

    def edge_search(self, source_label: str, target_label: str) -> Dict:
        """
        Returns the edge corresponding to the connection from the node with source_label to the node with target_label
        """
        for edge in self.graph.edges.data():
            edge_data = edge[2]
            if edge_data["source"] == source_label:
                if edge_data["target"] == target_label:
                    return edge

    def path_search(self, source_label: str, target_label: str) -> Tuple[List[Dict], List[Dict]]:
        """
        Returns the shortest path from the node corresponding to source_label to the node corresponding to target_label
        as a tuple of the list of traversed nodes and the list of traversed edges in the discovered path
        """
        source_id = self.get_node_id_from_label(source_label)
        target_id = self.get_node_id_from_label(target_label)
        traversed_node_ids = nx.shortest_path(self.graph, source_id, target_id)
        traversed_edges = self.path_edges(traversed_node_ids)
        return [self.get_node_from_id(node_id) for node_id in traversed_node_ids], traversed_edges

    def specific_path_search(self, edge_type: str, source_label, target_label):
        """
        Returns the shortest path from source to target for the subgraph containing only the edges
        of the type edge_type
        """
        source_id = self.get_node_id_from_label(source_label)
        target_id = self.get_node_id_from_label(target_label)
        edges = []
        for edge in self.graph.edges.data():
            edge_data = edge[2]
            if edge_data["type"] == edge_type:
                edges.append(edge)
        subgraph = self.graph.edge_subgraph(edges)
        traversed_node_ids = nx.shortest_path(subgraph, source_id, target_id)
        traversed_edges = self.path_edges(traversed_node_ids)
        return [self.get_node_from_id(node_id) for node_id in traversed_node_ids], traversed_edges

    def multistep_search(self, source_label: str, target_label: str, common_node_label: str = "pump_1"):
        """
        Returns a tuple featuring the shortest path from the node of source_label to the node of common_node_label, and
        the shortest path from the node of target_label to the node of common_node_label.
        """
        source_to_common = self.path_search(source_label, common_node_label)
        target_to_common = self.path_search(target_label, common_node_label)
        return source_to_common, target_to_common

    def specific_multistep_search(self, edge_type: str, source_label: str, target_label: str, common_node_label: str = "pump_1"):
        source_to_common = self.specific_path_search(edge_type, source_label, common_node_label)
        target_to_common = self.specific_path_search(edge_type, target_label, common_node_label)
        return source_to_common, target_to_common

    def path_edges(self, traversed_node_ids: List[int]) -> List[Dict]:
        """
        Returns a list of edges traversed for a list of traversed nodes.
        """
        traversed_edges = []
        for node, next_node in zip(traversed_node_ids[0:], traversed_node_ids[1:]):
            traversed_edges.append(self.graph[node][next_node])
        return traversed_edges

    def get_node_from_id(self, node_id) -> Dict:
        """
        Returns a node dictionary from its corresponding node id.
        """
        return self.graph.nodes[node_id]

    def get_node_id_from_label(self, label: str) -> int:
        """
        Returns a node id from a node label.
        """
        for node_id in self.graph.nodes:
            if self.graph.nodes[node_id]["label"] == label:
                return node_id

    def get_connected_nodes(self, label: str) -> List[Dict]:
        """
        Returns the nodes directly connected to a node corresponding to label as a list.
        """
        node_id = self.get_node_id_from_label(label)
        neighbor_ids = list(nx.all_neighbors(self.graph, node_id))
        return [self.get_node_from_id(node_id) for node_id in neighbor_ids]

    def dirtiest_path(self, edge_type: str, wash_label: str, waste_label: str = "waste", pump_label: str = "pump_1"):
        """
        Returns the path involving the most dirty tubes between a source wash solution and a target waste.
        """
        source_id = self.get_node_id_from_label(wash_label)
        target_id = self.get_node_id_from_label(waste_label)
        edges = []
        for edge in self.graph.edges.data():
            edge_data = edge[2]
            if edge_data["type"] == edge_type:
                edges.append(edge)
        subgraph = self.graph.edge_subgraph(edges)
        intermediate_traversed_node_ids = nx.bellman_ford_path(subgraph, source_id, pump_label, "clean")
        intermediate_traversed_edges = self.path_edges(intermediate_traversed_node_ids)
        source_to_common = self.get_node_from_id(intermediate_traversed_node_ids), intermediate_traversed_edges
        common_to_target_node_ids = nx.bellman_ford_path(subgraph, pump_label, target_id, "clean")
        common_to_target_edges = self.path_edges(common_to_target_node_ids)
        common_to_target = self.get_node_from_id(common_to_target_node_ids), common_to_target_edges
        return source_to_common, common_to_target

    def search_graph_for_edge_attr(self, edge_attribute: str, wanted_attribute: str):
        for edge in self.graph.edges.data():
            edge_data = edge[2]
            if edge_data[edge_attribute] == wanted_attribute:
                return edge

    def get_all_edge_data(self):
        all_edges = [edge for edge in self.graph.edges.data()]
        return all_edges


def cli_main():
    search = GraphSearch(GRAPH_JSON)

    b = search.path_search("rxn_1", "pump_1")
    print(b)

    #
    # next_node = search.single_search("rxn_1", True)
    #
    # print("hi")
    # a = search.multistep_search("sln_1", "rxn_1")
    #print(search.get_connected_nodes("rxn_1"))
    # print(search.edge_search("rxn_1", "pump_1"))
    pass

if __name__ == "__main__":
    cli_main()
    print('done')