import networkx as nx
import json
import pkg_resources
import pickle
import matplotlib.pyplot as plt
from themachine_pycontrol.drivers.vessel import Vessel
from themachine_pycontrol.drivers.hotplate import Hotplate
from themachine_pycontrol.drivers.valve import Valve
from themachine_pycontrol.drivers.pump import PumpModule

GRAPH_JSON = pkg_resources.resource_filename(
    "themachine_pycontrol", "graphgen/graph.json"
)

PUMP_MOD = PumpModule()


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


    def generate_graph(self) -> nx.Graph:
        """
        Reads the .json data which is used to generate the graph with nodes and edges that access classes in ~/drivers.
        Creates a directed graph object.
        """
        graph = nx.DiGraph()
        # TODO: Make getting the data its own function. It later on you want to use something other than JSON, it will
        #   harder to change.
        json_data = json.load(open(self.json_path))
        for node in json_data["nodes"]:
            node_id = node["id"]
            class_num = node["class_num"]
            volume = node["volume"]
            com_num = node["com_num"]
            max_volume = node["max_volume"]
            # TODO: This would be a great opportunity to include a factory pattern.
            if node["class"] == "Vessel":
                node["object"] = Vessel(float(max_volume), volume)
            elif node["class"] == "Hotplate":
                node["object"] = Hotplate(class_num, com_num)
            elif node["class"] == "Valve":
                node["object"] = Valve(class_num, com_num)
            elif node["class"] == "Pump":
                node["object"] = PUMP_MOD.pump(class_num)
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

