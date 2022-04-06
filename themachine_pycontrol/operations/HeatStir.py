import pkg_resources
import pickle
import networkx as nx
from themachine_pycontrol.main.graph_search import GraphSearch

GRAPH_PKL = pkg_resources.resource_filename(
    "themachine_pycontrol", "graphgen/graph.pkl"
)

SEARCH = GraphSearch(GRAPH_PKL)


class HeatStir:
    def __init__(self, search: GraphSearch, object_label: str, temp: int, rpm: int):
        self.search = search
        self.object_label = object_label
        self.temp = temp
        self.rpm = rpm
        self.hotplate = self.find_hotplate()

    def __call__(self):
        self.heat_stir()

    def find_hotplate(self):
        neighbors = self.search.get_connected_nodes(self.object_label)
        for node in neighbors:
            if node["class"] == "Hotplate":
                a = node["object"]
                return node["object"]
            pass

    def heat(self):
        self.hotplate.heat(True, self.temp)
        pass

    def stir(self):
        self.hotplate.stir(True, self.rpm)

    def heat_stir(self):
        self.heat()
        self.stir()


def cli_main():
    graph_1 = GraphSearch(GRAPH_PKL)
    try_1 = HeatStir(SEARCH, "rxn_1", 30, 120)
    try_1.heat()


if __name__ == "__main__":
    cli_main()

