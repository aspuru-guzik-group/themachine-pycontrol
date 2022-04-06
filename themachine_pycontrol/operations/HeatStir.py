import pkg_resources
import networkx as nx
from themachine_pycontrol.main.graph_search import GraphSearch
from themachine_pycontrol.graphgen.generator import Generator


GRAPH_JSON = pkg_resources.resource_filename(
    "themachine_pycontrol", "graphgen/graph.json"
)


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
                print(a)
                return node["object"]

    def heat(self):
        self.hotplate.heat(True, self.temp)

    def stir(self):
        self.hotplate.stir(True, self.rpm)

    def heat_stir(self):
        self.heat()
        self.stir()


def cli_main():
    graph_1_gen = Generator(GRAPH_JSON)
    graph_1 = graph_1_gen.generate_graph()
    search = GraphSearch(graph_1)
    try_1 = HeatStir(search, "rxn_1", 30, 120)
    try_1.heat_stir()


if __name__ == "__main__":
    cli_main()

