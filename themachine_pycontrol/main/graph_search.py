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
        file = open(graph_path, "rb")
        self.graph = pickle.load(file)
        file.close()


def cli_main():
    search = GraphSearch(GRAPH_PKL)
    print(search.graph)


if __name__ == "__main__":
    cli_main()
