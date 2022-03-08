import networkx as nx
import json
import pkg_resources
import pickle
from themachine_pycontrol.drivers.vial import Container
from themachine_pycontrol.drivers.hotplate import Hotplate
from themachine_pycontrol.drivers.valve import Valve

GRAPH_JSON = pkg_resources.resource_filename(
    "themachine_pycontrol", "graphgen/graph.json"
)

GRAPH_PKL = pkg_resources.resource_filename(
    "themachine_pycontrol", "graphgen/graph.pkl"
)


class Generator:
    """
    Class that contains the functions for generating the graph that represents the hardware in The Machine.

    === Public Attributes ==


    === Representation Invariants ===
    - 
    """

    def __init__(self, json_path: str, graph_path: str) -> None:
        """
        Initializes Generator class with paths to where data is stored, and where graph is stored.
        """
        self.json_path = json_path
        self.graph_path = graph_path

    def graph_to_pkl(self, graph, pkl_path):
        file = open(pkl_path, "wb")
        pickle.dump(graph, file)
        file.close()

    def generate_graph(self) -> nx.Graph:
        """
        Reads the .json data which is used to generate the graph with nodes and edges that access classes in ~/drivers.
        """
        graph = nx.Graph()
        json_data = json.load(open(self.json_path))
        id = 0
        for node in json_data["nodes"]:
            node_id = id
            type_num = node["type_num"]
            volume = node["volume"]
            com_num = node["com_num"]
            max_volume = node["max_volume"]
            if node["class"] == "Container":
                node["object"] = Container(float(max_volume), volume)
            elif node["class"] == "Hotplate":
                # node["object"] = Hotplate(type_num)
                node["object"] = "hotplate"
            elif node["class"] == "Valve":
                node["object"] = Valve(type_num, com_num)
            graph.add_nodes_from([(node_id, node)])
            id += 1
        for link in json_data["links"]:
            source = link["source"]
            target = link["target"]
            for node_id in graph.nodes:  # iterate through node_ids from the graph
                node = graph.nodes[node_id]  # get node from graph with node_id
                if node["label"] == source:
                    source_id = node["id"]
                elif node["label"] == target:
                    target_id = node["id"]
            graph.add_edge(source_id, target_id, data=link)

        # stores graph in a .pkl file
        self.graph_to_pkl(graph, self.graph_path)

        return graph

    def index_nodes(self):
        graph_json = json.load(open(self.json_path))
        id = 0
        for node in graph_json["nodes"]:
            node["id"] = id
            id += 1

        f = open(self.json_path, "w")
        json.dump(graph_json, f)
        f.close()


def cli_main():
    generator = Generator(GRAPH_JSON, GRAPH_PKL)
    new_graph = generator.generate_graph()
    for edge_id in new_graph.edges:
        edge = new_graph.edges[edge_id]
        print(edge["data"])
    # print("done")
    # graph.index_nodes()


if __name__ == "__main__":
    cli_main()


# TODO: pyvisa / visa???
# TODO: create all links
# TODO: label nodes correctly under "label"
# TODO: edge data weird formatting
