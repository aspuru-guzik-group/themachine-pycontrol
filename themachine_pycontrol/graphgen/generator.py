import networkx as nx
import json
import pkg_resources
import pickle
import matplotlib.pyplot as plt
from themachine_pycontrol.drivers.vessel import Vessel
from themachine_pycontrol.drivers.hotplate import Hotplate
from themachine_pycontrol.drivers.valve import Valve
from themachine_pycontrol.drivers.pump import PumpModule
from themachine_pycontrol.drivers.relay import RelayModule, Relay

GRAPH_JSON = pkg_resources.resource_filename(
    "themachine_pycontrol", "graphgen/graph.json"
)


class Generator:
    """
    Class that contains the functions for generating the graph that represents the hardware in The Machine.

    === Public Attributes ==
    json_path: the path for accessing the JSON file, where graph dictionaries are stored

    """

    def __init__(self, json_path: str) -> None:
        """
        Initializes Generator class with paths to where data is stored, and where graph is stored.
        """
        self.json_path = json_path

    def __call__(self):
        """
        When a Generator object is called, ex: generator_1(), the generate_graph() function is called
        """
        self.generate_graph()

    def _make_vessel(self, node) -> Vessel:
        """
        Returns a vessel object given a vessel node.
        """
        volume = node["volume"]
        max_volume = node["max_volume"]
        return Vessel(float(max_volume), volume)

    def _make_hotplate(self, node) -> Hotplate:
        """
        Returns a hotplate object given a hotplate node.
        """
        class_num = node["class_num"]
        com_num = node["com_num"]
        return Hotplate(class_num, com_num)

    def _make_valve(self, node) -> Valve:
        """
        Returns a valve object given a valve node.

        """
        class_num = node["class_num"]
        com_num = node["com_num"]
        return Valve(class_num, com_num)

    def _make_pump(self, node) -> Pump:
        """
        Returns a pump object given a pump node.
        """
        class_num = node["class_num"]
        return Pump(class_num)

    def _make_relay(self, node) -> Relay:
        """
        Returns a relay object given a relay node.
        """
        class_num = node["class_num"]
        com_num = node["com_num"]
        mod_address = node["module_address"]
        return Relay(class_num, com_num, mod_address)

    def factory(self, node_class: str, node):
        """
        Given a node of any type, creates the correct corresponding object and updates the node dictionary
        to include this object.
        """

        classes = {
            "Vessel":  self._make_vessel(node),
            "Hotplate": self._make_hotplate(node),
            "Valve": self._make_valve(node),
            "Pump": self._make_pump(node),
            "Relay": self._make_relay(node)
        }
        node["object"] = classes[node_class]

    def get_data(self):
        json.load(open(self.json_path))

    def generate_graph(self) -> nx.Graph:
        """
        Reads the .json data which is used to generate the graph with nodes and edges that access classes in ~/drivers.
        Creates a directed graph object.
        """
        graph = nx.DiGraph()
        node_id = node["id"]
        json_data = self.get_data()
        for node in json_data["nodes"]:
            node_class = node["class"]
            self.factory(node_class, node)
            graph.add_nodes_from([(node_id, node)])
        for link in json_data["links"]:
            source = link["source"]
            target = link["target"]
            for node_id in graph.nodes:  # iterate through node_ids from the graph
                node = graph.nodes[node_id]  # get node from graph with node_id
                if node["label"] == source:
                    source_id = node["id"]
                elif node["label"] == target:
                    target_id = node["id"]
            graph.add_edge(
                source_id,
                target_id,
                id=link["id"],
                name=link["name"],
                source=link["source"],
                target=link["target"],
                type=link["type"],
                port_num=link["port_num"],
            )
        return graph

    def index_nodes(self) -> None:
    """
    Renumbers the node ids in the JSON automatically.
    """
        graph_json = json.load(open(self.json_path))
        id = 0
        for node in graph_json["nodes"]:
            node["id"] = id
            id += 1

        with open(self.json_path, "w") as f:
            json.dump(graph_json, f)


def cli_main():
    generator = Generator(GRAPH_JSON)
    new_graph = generator.generate_graph()
    for edge_id in new_graph.edges:
        new_graph.edges[edge_id]
    nx.draw_planar(new_graph, with_labels=True)
    plt.show()


if __name__ == "__main__":
    cli_main()

