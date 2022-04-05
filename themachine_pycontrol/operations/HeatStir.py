import pkg_resources
import pickle
import networkx as nx


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
                return node["object"]

    def heat(self):
        self.hotplate.heat(True, self.temp)

    def stir(self):
        self.hotplate.stir(True, self.rpm)

    def heat_stir(self):
        self.heat()
        self.stir()



