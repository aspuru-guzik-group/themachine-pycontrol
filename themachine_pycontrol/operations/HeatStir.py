import pkg_resources
from themachine_pycontrol.graph.search import GraphSearch
from themachine_pycontrol.graph.generator import Generator


GRAPH_JSON = pkg_resources.resource_filename(
    "themachine_pycontrol", "graph/graph.json"
)


class HeatStir:
    """
    Class that contains the functions for heating/stirring hotplates across the graph representing the Machine.

    === Public Attributes ==
    search: the GraphSearch object that will be used to perform graph search operations
    object_label: the label of the node corresponding to the object to be heated/stirred
    temp: the desired target temperature of the hotplate connected to the object
    rpm: the desired target stir speed (in rpm) of the hotplate connected to the object

    === Representation Invariants ===
    - temp must be <340 degrees C
    - rpm must be <1700 rpm
    """
    def __init__(self, search: GraphSearch, object_label: str, temp: int, rpm: int):
        # TODO: This will set heat/stir N times for N vials on the same hotplate.
        """
        Instantiates a HeatStir object. This will set the heat/stir conditions for all vials on the same hotplate.
        """
        self.search = search
        self.object_label = object_label
        self.temp = temp
        self.rpm = rpm
        self.hotplate = self.find_hotplate()

    def __call__(self):
        """
        When a HeatStir object is called, ex: heatstir_1(), the heat_stir() function is called.
        """
        self.heat_stir()

    def find_hotplate(self) -> Hotplate:
        """
        Returns the hotplate corresponding to the node with the label object_label
        """
        neighbors = self.search.get_connected_nodes(self.object_label)
        for node in neighbors:
            if node["class"] == "Hotplate":
                a = node["object"]
                print(a)
                return node["object"]

    def heat(self):
        """
        Heats self.hotplate to temp.
        """
        self.hotplate.heat(True, self.temp)

    def stir(self):
        """
        Stirs self.hotplate at rpm.
        """
        self.hotplate.stir(True, self.rpm)

    def heat_stir(self):
        """
        Heats and stirs hotplate at temp and rpm.
        """
        self.heat()
        self.stir()


def main():
    graph_1_gen = Generator(GRAPH_JSON)
    graph_1 = graph_1_gen.generate_graph()
    search = GraphSearch(graph_1)
    try_1 = HeatStir(search, "rxn_1", 30, 120)
    try_1()


if __name__ == "__main__":
    main()
