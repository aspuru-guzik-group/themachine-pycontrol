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
            else:
                if edge_data["target"] == label:
                    traversed_nodes.append((edge[0], edge[1]))
                    src_node = self.graph.nodes[edge[0]]
                    tgt_node = self.graph.nodes[edge[1]]

        return tgt_node["label"]

        # elif edge_data["target"] == tgt_label:
        # print(edge_data["id"])

    def multistep_search(self):
        # NOTE: For later, talk with Han!
        pass


def cli_main():
    search = GraphSearch(GRAPH_PKL)
    next_node = search.single_search("valve_4", True)
    print(next_node)


if __name__ == "__main__":
    cli_main()
