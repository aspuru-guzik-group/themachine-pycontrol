import pkg_resources
import pickle
import networkx as nx
from typing import Dict, List, Tuple

# TODO: I think we can remove this line now that the JSON path is passed in the Generator init.
GRAPH_JSON = pkg_resources.resource_filename(
    "themachine_pycontrol", "graph/graph.json"
)


class GraphSearch:
    """
    Class that contains the functions for searching the graph representing the Machine.
    === Public Attributes ==
    graph: the graph object that search operations will be performed on
    """

    def __init__(self, graph: nx.DiGraph):
        """
        Instantiates a GraphSearch object for a graph
        """
        self.graph = graph

    # FIXME: Already implemented as Graph.get_edge_data
    # Have this because transfer() doesn't actually require a Graph attribute input, it just uses a GraphSearch object which it aleready needs
    # so this function saves one input attribute in transfer()
    # def edge_search(self, source_label: str, target_label: str) -> Dict:
    #     """
    #     Returns the edge corresponding to the connection from the node with source_label to the node with target_label
    #     """
    #     for edge in self.graph.edges.data():
    #         edge_data = edge[2]
    #         if edge_data["source"] == source_label:
    #             if edge_data["target"] == target_label:
    #                 return edge

    # def path_search(self, source_label: str, target_label: str) -> Tuple[List[Dict], List[Dict]]:
    #     """
    #     Returns the shortest path from the node corresponding to source_label to the node corresponding to target_label
    #     as a tuple of the list of traversed nodes and the list of traversed edges in the discovered path
    #     """
    #     source_id = self.get_node_id_from_label(source_label)
    #     target_id = self.get_node_id_from_label(target_label)
    #     traversed_node_ids = nx.shortest_path(self.graph, source_id, target_id)
    #     traversed_edges = self.path_edges(traversed_node_ids)
    #     return [self.get_node_from_id(node_id) for node_id in traversed_node_ids], traversed_edges

    def specific_path_search(self, edge_type: str, source_label: str, target_label: str) -> tuple[list[dict], list[dict]]:
        """
        Returns the shortest path from source to target for the subgraph containing only the edges
        of the type edge_type
        """
        # TODO: Lines 55-56 and 64-65 are in path_search(), specific_path_search() and dirtiest_path().
        #  Should also be refactored to be a single method and called in all 3.
        source_id = self.get_node_id_from_label(source_label)
        target_id = self.get_node_id_from_label(target_label)
        subgraph = self.edge_type_subgraph(edge_type)
        traversed_node_ids = nx.shortest_path(subgraph, source_id, target_id)
        traversed_edges = self.path_edges(traversed_node_ids)
        return [self.get_node_from_id(node_id) for node_id in traversed_node_ids], traversed_edges

    def edge_type_subgraph(self, edge_type: str) -> graph:
        """
        Returns a subgraph containing only edges of the type edge_type.
        """
        edges = []
        for edge in self.graph.edges.data():
            edge_data = edge[2]
            if edge_data["type"] == edge_type:
                edges.append(edge)
        subgraph = self.graph.edge_subgraph(edges)
        return subgraph

    # def multistep_search(self, source_label: str, target_label: str, common_node_label: str = "pump_1"):
    #     """
    #     Returns a tuple featuring the shortest path from the node of source_label to the node of common_node_label, and
    #     the shortest path from the node of target_label to the node of common_node_label.
    #     """
    #     source_to_common = self.path_search(source_label, common_node_label)
    #     target_to_common = self.path_search(target_label, common_node_label)
    #     return source_to_common, target_to_common

    def specific_multistep_search(self, edge_type: str, source_label: str, target_label: str, common_node_label: str = "pump_1"):
        """
        Returns a tuple featuring the shortest path from the node of source_label to the node of common_node_label, and
        the shortest path from the node of target_label to the node of common_node_label, using edges only of the type
        edge_type.
        """
        # TODO: Doc (and type) me!
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

    def get_node_from_id(self, node_id) -> dict:
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

    def weighted_specific_path_search(self, edge_type: str, source_label: str, target_label: str) -> tuple[list[dict], list[dict]]:
        """
        Returns the shortest weighted path from source to target for the subgraph containing only the edges
        of the type edge_type
        """
        source_id = self.get_node_id_from_label(source_label)
        target_id = self.get_node_id_from_label(target_label)
        subgraph = self.edge_type_subgraph(edge_type)
        traversed_node_ids = nx.bellman_ford_path(subgraph, source_id, target_id, "clean")
        traversed_edges = self.path_edges(traversed_node_ids)
        return [self.get_node_from_id(node_id) for node_id in traversed_node_ids], traversed_edges

    def weighted_multistep_search(self,  edge_type: str, source_label: str, target_label: str, pump_label: str = "pump_1") \
            -> Tuple[Tuple[Dict, List[Dict]], Tuple[Dict, List[Dict]]]:
        """
        Returns a tuple featuring the shortest weighted path from the node of source_label to the node of common_node_label, and
        the shortest path from the node of target_label to the node of common_node_label, using edges only of the type
        edge_type.
        """
        source_to_common = self.weighted_specific_path_search(edge_type, source_label, pump_label)
        target_to_common = self.weighted_specific_path_search(edge_type, target_label, common_node_label)
        return source_to_common, target_to_common

    def dirtiest_path(self, edge_type: str, wash_label: str, waste_label: str = "waste", pump_label: str = "pump_1")\
            -> Tuple[Tuple[Dict, List[Dict]], Tuple[Dict, List[Dict]]]:
        """
        Returns the path involving the most dirty tubes between a source wash solution and a target waste.
        """
        return self.weighted_multistep_search(edge_type, wash_label, waste_label, pump_label)

    def get_all_edge_data(self) -> list[dict]:
        """
        Returns a list of all edges in a graph
        """
        return [edge for edge in self.graph.edges.data()]


def main():
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
    main()
    print('done')
