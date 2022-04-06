import pkg_resources
import pickle
import networkx as nx
from typing import Dict, List, Tuple

GRAPH_JSON = pkg_resources.resource_filename(
    "themachine_pycontrol", "graphgen/graph.json"
)

# TODO: Typehinting!


class GraphSearch:
    """
    pass
    """

    def __init__(self, graph):
        """
        pass
        """
        # with open(graph_path, "rb") as f:
        #     self.graph = pickle.load(f)
        self.graph: nx.DiGraph = graph

    # FIXME: Is this return type correct?
    def single_search(self, label: str, fwd: bool) -> str:
        """
        label:
        fwd:

        # -> list[tuple(int, int)]
        # NOTE: for unordered graph: node labels from edge are not in order of (source, target)
        Search through graph from first source to final target
        """
        traversed_nodes = []
        for edge in self.graph.edges.data():
            edge_data = edge[2]
            if fwd:
                if edge_data["source"] == label:
                    traversed_nodes.append((edge[0], edge[1]))
                    src_node = self.graph.nodes[edge[0]]
                    tgt_node = self.graph.nodes[edge[1]]
                    return tgt_node
            else:
                if edge_data["target"] == label:
                    traversed_nodes.append((edge[1], edge[0]))
                    src_node = self.graph.nodes[edge[1]]
                    tgt_node = self.graph.nodes[edge[0]]
                    return tgt_node


        # elif edge_data["target"] == tgt_label:
        # print(edge_data["id"])

    # TODO: Typehint return
    def edge_search(self, source_label: str, target_label: str):
        """

        """
        for edge in self.graph.edges.data():
            edge_data = edge[2]
            if edge_data["source"] == source_label:
                if edge_data["target"] == target_label:
                    return edge

    # def get_edge(self, id):
    #     """
    #
    #     """
    #     for edge in self.graph.edges.data():
    #         edge_data = edge[2]
    #         if edge_data["id"] == id:
    #             return edge

    # def multistep_search(self, source_label: str, target_label: str) -> list:
    #     # NOTE: For later, talk with Han!
    #     traversed_nodes = []
    #     stop_1 = self.single_search(source_label, True)
    #     stop_1_label = stop_1["label"]
    #     print(stop_1)
    #     #traversed_nodes.append(source_label)
    #     traversed_nodes.append(stop_1)
    #     #int_2 = self.graph.edges.data[4]
    #     #edge_1_id = self.edge_search(source_label, int_1)
    #     #edge_1 = self.get_edge(edge_1_id)
    #     #int_2 = edge_1[1]
    #     #traversed_nodes.append(int_2)
    #     stop_2 = self.single_search(stop_1_label, True) #should give pump
    #     print(stop_2)
    #     traversed_nodes.append(stop_2)
    #     stop_a = self.single_search(target_label, True)
    #     stop_b = self.single_search(stop_a, True)
    #     #traversed_nodes.append(int_b)
    #     traversed_nodes.append(stop_a)
    #     #traversed_nodes.append(target_label)
    #     return traversed_nodes

    def path_search(self, source_label: str, target_label: str) -> Tuple[List[Dict], List[Dict]]:
        source_id = self.get_node_id_from_label(source_label)
        target_id = self.get_node_id_from_label(target_label)
        traversed_node_ids = nx.shortest_path(self.graph, source_id, target_id)
        traversed_edges = self.path_edges(traversed_node_ids)
        return [self.get_node_from_id(node_id) for node_id in traversed_node_ids], traversed_edges

    def multistep_search(self, source_label: str, target_label: str, common_node_label: str = "pump_1"):
        source_to_common = self.path_search(source_label, common_node_label)
        target_to_common = self.path_search(target_label, common_node_label)
        return source_to_common, target_to_common

    def path_edges(self, traversed_node_ids: List[int]):
        traversed_edges = []
        for node, next_node in zip(traversed_node_ids[0:], traversed_node_ids[1:]):
            traversed_edges.append(self.graph[node][next_node])
        return traversed_edges

    def multistep_edges(self, source_label: str, target_label: str) -> list:
        traversed_edges = []
        traversed_nodes = self.multistep_search(source_label, target_label)
        traversed_edges.append(self.edge_search(source_label, traversed_nodes[0]))
        traversed_edges.append(self.edge_search(traversed_nodes[0], traversed_nodes[1]))
        traversed_edges.append(self.edge_search(traversed_nodes[1], traversed_nodes[2]))
        traversed_edges.append(self.edge_search(traversed_nodes[2], target_label))
        return traversed_edges

    def get_node_from_id(self, node_id):
        return self.graph.nodes[node_id]
        # for node in self.graph.nodes:
        #     if node["id"] == node_id:
        #         return node

    def get_node_id_from_label(self, label: str):
        for node_id in self.graph.nodes:
            if self.graph.nodes[node_id]["label"] == label:
                return node_id

    def get_connected_nodes(self, label: str):
        node_id = self.get_node_id_from_label(label)
        neighbor_ids = list(nx.all_neighbors(self.graph, node_id))
        return [self.get_node_from_id(node_id) for node_id in neighbor_ids]


def cli_main():
    search = GraphSearch(GRAPH_JSON)

    bla = search.path_search("rxn_1", "pump_1")
    print(bla)
    
    #
    # next_node = search.single_search("rxn_1", True)
    #
    # print("hi")
    # a = search.multistep_search("sln_1", "rxn_1")
    print(search.get_connected_nodes("rxn_1"))


if __name__ == "__main__":
    cli_main()
    print('done')
