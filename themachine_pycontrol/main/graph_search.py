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
                    return tgt_node["label"]
            else:
                if edge_data["target"] == label:
                    traversed_nodes.append((edge[1], edge[0]))
                    src_node = self.graph.nodes[edge[1]]
                    tgt_node = self.graph.nodes[edge[0]]
                    return tgt_node["label"]


        # elif edge_data["target"] == tgt_label:
        # print(edge_data["id"])

    def edge_search(self, source_label: str, target_label: str):
        """

        """
        for edge in self.graph.edges.data():
            edge_data = edge[2]
            if edge_data["source"] == source_label:
                if edge_data["target"] == target_label:
                    return edge_data["id"]

    def get_edge(self, id):
        """

        """
        for edge in self.graph.edges.data():
            edge_data = edge[2]
            if edge_data["id"] == id:
                return edge

    def multistep_search(self, source_label: str, target_label: str):
        # NOTE: For later, talk with Han!
        traversed_nodes = []
        int_1 = self.single_search(source_label, True)
        print(int_1)
        traversed_nodes.append(int_1)
        #int_2 = self.graph.edges.data[4]
        #edge_1_id = self.edge_search(source_label, int_1)
        #edge_1 = self.get_edge(edge_1_id)
        #int_2 = edge_1[1]
        #traversed_nodes.append(int_2)
        int_2 = self.single_search(int_1, True) #should give pump
        traversed_nodes.append(int_2)
        int_a = self.single_search(target_label, True)
        int_b = self.single_search(int_a, True)
        traversed_nodes.append(int_b)
        traversed_nodes.append(int_a)
        return traversed_nodes

        #traversed_nodes.append(self.graph.edges.data)


def cli_main():
    search = GraphSearch(GRAPH_PKL)
    next_node = search.single_search("rxn_1", True)
    print(next_node)
    test = search.edge_search("valve_1","rxn_1")
    print("here")
    print(test)
    #lst = search.graph.write.edgelist()
    #print(lst[0])
    print(type(search.graph.edges.data()))
    print(type(search.graph.nodes.data()))
    #print((search.graph.edges[0]))
    #for edge in search.graph.edges.data():
        #print(edge)
    #for edge in search.graph.nodes():
     #   print(edge)
    print(search.multistep_search("soln_1", "rxn_1"))




if __name__ == "__main__":
    cli_main()
