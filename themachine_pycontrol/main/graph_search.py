import pkg_resources
import pickle

GRAPH_PKL = pkg_resources.resource_filename(
    "themachine_pycontrol", "graphgen/graph.pkl"
)


class GraphSearch:
    """
    pass
    """

    def __init__(self, graph_path):
        """
        pass
        """
        with open(graph_path, "rb") as f:
            self.graph = pickle.load(f)

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

    def multistep_search(self, source_label: str, target_label: str) -> list:
        # NOTE: For later, talk with Han!
        traversed_nodes = []
        stop_1 = self.single_search(source_label, True)
        stop_1_label = stop_1["label"]
        print(stop_1)
        #traversed_nodes.append(source_label)
        traversed_nodes.append(stop_1)
        #int_2 = self.graph.edges.data[4]
        #edge_1_id = self.edge_search(source_label, int_1)
        #edge_1 = self.get_edge(edge_1_id)
        #int_2 = edge_1[1]
        #traversed_nodes.append(int_2)
        stop_2 = self.single_search(stop_1_label, True) #should give pump
        print(stop_2)
        traversed_nodes.append(stop_2)
        stop_a = self.single_search(target_label, True)
        stop_b = self.single_search(stop_a, True)
        #traversed_nodes.append(int_b)
        traversed_nodes.append(stop_a)
        #traversed_nodes.append(target_label)
        return traversed_nodes

    def multistep_edges(self, source_label: str, target_label: str) -> list:
        traversed_edges = []
        traversed_nodes = self.multistep_search(source_label, target_label)
        traversed_edges.append(self.edge_search(source_label, traversed_nodes[0]))
        traversed_edges.append(self.edge_search(traversed_nodes[0], traversed_nodes[1]))
        traversed_edges.append(self.edge_search(traversed_nodes[1], traversed_nodes[2]))
        traversed_edges.append(self.edge_search(traversed_nodes[2], target_label))
        return traversed_edges

    def get_node_from_id(self, node_id):
        for node in self.graph.nodes():
            if node["id"] == node_id:
                return node

    def get_node_from_label(self, label: str):
        for node in self.graph.nodes():
            if node["label"] == label:
                return node





def cli_main():
    search = GraphSearch(GRAPH_PKL)
    next_node = search.single_search("rxn_1", True)
    #print(next_node)
    #test = search.edge_search("valve_1","rxn_1")
    #print("here")
    #print(test)
    #lst = search.graph.write.edgelist()
    #print(lst[0])
    #print(type(search.graph.edges.data()))
    #print(type(search.graph.nodes.data()))
    #print((search.graph.edges[0]))
    #for edge in search.graph.edges.data():
        #print(edge)
    #for edge in search.graph.nodes():
     #   print(edge)
    print(search.multistep_search("sln_1", "rxn_1"))
    # ex_edge = search.get_edge(1)
    # print(ex_edge[2]["port_num"])
    # str_tuple = ex_edge[2]["port_num"]
    # tuple_tuple = eval(str_tuple)
    # port = tuple_tuple[1]
    # print(port)
    # print(search.multistep_edges("sln_1", "rxn_1"))
    # #print(search.get_node(0))
    # print("!")
    # for node in search.graph.nodes.data():
    #     print(node)
    # node_ex = search.get_node(0)
    # print(node_ex)
    # print(node_ex[1]["label"])
    print("hotplate test")
    # hotplate = search.single_search("rxn_1", False)
    # print(hotplate)
    # print(hotplate["object"])
    # hotplate["object"].heat(True, 20)
    print("new test")
    x = search.single_search("rxn_1", True)
    print(x)
    print(x["object"])
    x["object"].move(2)






if __name__ == "__main__":
    cli_main()
