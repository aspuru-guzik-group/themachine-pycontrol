from pathlib import Path
from typing import Dict

import networkx as nx
import json
import pkg_resources
import pickle
import matplotlib.pyplot as plt
# TODO: Look in __all__ attribute of __init__.py files so that you can do this:
#  from themachine_pycontrol.drivers import Hotplate, Pump, Relay, Vessel
#  instead of needing individual lines for each module.
# from themachine_pycontrol.drivers.vessel import Vessel
# from themachine_pycontrol.drivers.hotplate import Hotplate
# from themachine_pycontrol.drivers.valve import Valve
# from themachine_pycontrol.drivers.pump import Pump
# from themachine_pycontrol.drivers.relay import Relay
from themachine_pycontrol.drivers import Hotplate, Pump, Relay, Valve, Vessel

# TODO: I think we can remove this line now that the JSON path is passed in the Generator init.
# ^ this is used to test the code/to generate the graph
GRAPH_JSON = pkg_resources.resource_filename(
    "themachine_pycontrol", "graph/graph.json"
)


class NodeFactory:
    """

    """
    def __init__(self, node: dict):
        self.node = node
        self.volume = self.node["volume"]
        self.max_volume = self.node["max_volume"]
        self.class_num = self.node["class_num"]
        self.com_num = self.node["com_num"]
        self.mod_address = self.node["module_address"]
        self.node_class = self.node["class"]
        self.addable = self.node["addable"]
        self.removable = self.node["removable"]

    def _make_vessel(self) -> Vessel:
        """
        Returns a vessel object given a vessel node.
        """
        return Vessel(float(self.max_volume), self.volume, self.addable, self.removable)

    def _make_hotplate(self) -> Hotplate:
        """
        Returns a hotplate object given a hotplate node.
        """
        return Hotplate(self.com_num)

    def _make_valve(self) -> Valve:
        """
        Returns a valve object given a valve node.

        """
        return Valve(self.class_num, self.com_num)

    def _make_pump(self) -> Pump:
        """
        Returns a pump object given a pump node.
        """
        return Pump(self.class_num)

    def _make_relay(self) -> Relay:
        """
        Returns a relay object given a relay node.
        """
        return Relay(self.class_num, self.com_num, self.mod_address)

    def make_object(self):
        """
        Given a node of any type, creates the correct corresponding object and updates the node dictionary
        to include this object.
        """

        classes = {
            "Vessel":  self._make_vessel(),
            "Hotplate": self._make_hotplate(),
            "Valve": self._make_valve(),
            "Pump": self._make_pump(),
            "Relay": self._make_relay()
        }
        return classes[self.node_class]


class Generator:
    """
    Class that contains the functions for generating the graph that represents the hardware in The Machine.

    === Public Attributes ==
    json_path: the path for accessing the JSON file, where graph dictionaries are stored

    """

    def __init__(self, json_path: Path) -> None:
        """
        Initializes Generator class with paths to where data is stored, and where graph is stored.
        """
        self.json_path = json_path

    def __call__(self):
        """
        When a Generator object is called, ex: generator_1(), the generate_graph() function is called
        """
        self.generate_graph()

    def get_data(self) -> Dict:
        """
        Opens file path to where graph data is stored.
        """
        with open(self.json_path, 'r') as f:
            data = json.load(f)
        return data

    def generate_graph(self) -> nx.Graph:
        """
        Reads the .json data which is used to generate the graph with nodes and edges that access classes in ~/drivers.
        Creates a directed graph object.
        """
        graph = nx.DiGraph()
        json_data = self.get_data()
        for node in json_data["nodes"]:
            node_id = node["id"]
            node["object"] = NodeFactory(node).make_object()
            # node_factory = NodeFactory(node).make_object()
            # new_object = node_factory.factory()
            # node_factory.set_object(new_object)
            graph.add_nodes_from([(node_id, node)])
        for link in json_data["links"]:
            source = link["source"]
            target = link["target"]
            source_id, target_id = None, None
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
                clean=link["clean"]
            )
        return graph

    def index_nodes(self) -> None:
        """
        Renumbers the node ids in the JSON automatically. This allows you to more easily update the graph JSON.
        """
        graph_json = json.load(open(self.json_path))
        id = 0
        for node in graph_json["nodes"]:
            node["id"] = id
            id += 1

        with open(self.json_path, "w") as f:
            json.dump(graph_json, f)


def main():
    generator = Generator(GRAPH_JSON)
    new_graph = generator.generate_graph()
    for edge_id in new_graph.edges:  # FIXME: Huh? I actually have no idea but im scared to delete it
        new_graph.edges[edge_id]
    nx.draw_planar(new_graph, with_labels=True)
    plt.show()


if __name__ == "__main__":
    main()

