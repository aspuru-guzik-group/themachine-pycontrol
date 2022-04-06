import pkg_resources
import networkx as nx
import json
from themachine_pycontrol.drivers.vessel import Vessel
from themachine_pycontrol.drivers.hotplate import Hotplate
from themachine_pycontrol.drivers.valve import Valve
from themachine_pycontrol.graphgen.generator import Generator
from themachine_pycontrol.drivers.pump import Pump
from themachine_pycontrol.main.graph_search import GraphSearch
import typing

GRAPH_JSON = pkg_resources.resource_filename(
    "themachine_pycontrol", "graphgen/graph.json"
)


class Transfer:

    def __init__(self, search: GraphSearch, source: str, target: str, volume: float):
        self.common = "pump_1"  # Hard-coded for now...
        self.search = search
        self.draw_path, self.dispense_path = self.search.multistep_search(source, target, self.common)
        self.volume = volume

    def __call__(self):
        self.transfer_liquid()

    def transfer_liquid(self) -> None:

        self.move_liquid(self.draw_path, direction=True)
        self.move_liquid(self.dispense_path, direction=False)

    def move_liquid(self, path: tuple, direction: bool):
        """
        Draws liquid of given volume from the vessel corresponding to label.
        """
        nodes, edges = path
        self._set_valves(nodes, edges)
        self._pump_liquid(nodes, edges, direction)

    def _set_valves(self, nodes: list, edges: list):
        for node in nodes:
            if node["class"] == "Valve":
                for edge in edges: #can be improved with Path class
                    if edge["target"] == node["label"]:
                        valve_port = eval(edge["port_num"])[1]
                        node["object"].move(valve_port)

    def _pump_liquid(self, nodes: list, edges: list, direction: bool):
        for node in nodes:
            if node["class"] == "Pump":
                for edge in edges: #can be improved with Path class
                    if edge["target"] == node["label"]:
                        pump_port = edge["port_num"][1]
                        if direction:
                            node["object"].move(pump_port, 25, self.volume)
                        else:
                            node["object"].move(pump_port, 25, 0)

    # def transfer(graph_path, volume: int, source, target, wait_ready: bool):
    #     """
    #     Note: assumes source and target are rxn or sln vessels.
    #     """
    #     search = GraphSearch(graph_path)
    #     traversed_edges = search.multistep_edges(source, target)
    #     # for edge in traversed_edges:
    #     #     port_1_tuple = eval(edge[2]["port_num"])
    #     #     port_1 = port_1_tuple[1]
    #     #     search.get_node(edge[node["object"].move(port_1)
    #     traversed_nodes: list = search.multistep_search(source, target)
    #     for node in traversed_nodes:
    #         if node["label"] == traversed_nodes[0]:
    #             # edge_1 = search.edge_search(search.edge_search(source, node["label"]))
    #             edge_1 = traversed_edges[0]
    #             port_1_tuple = eval(edge_1[2]["port_num"])
    #             port_1 = port_1_tuple[1]
    #             node["object"].move(port_1)
    #             print(f"{traversed_nodes[0]} has been opened to port {port_1}.")
    #         elif node["label"] == traversed_nodes[2]:
    #             edge_4 = traversed_edges[3]
    #             port_4_tuple = eval(edge_4[2]["port_num"])
    #             port_4 = port_4_tuple[1]
    #             node["object"].move(port_4)
    #             print(f"{traversed_nodes[2]} has been opened to port {port_4}.")
    #         elif node["label"] == traversed_nodes[1]:
    #             edge_2 = traversed_edges[1]
    #             edge_3 = traversed_edges[2]
    #             port_2_tuple = eval(edge_2[2]["port_num"])  # src valve to pump
    #             port_3_tuple = eval(edge_3[2]["port_num"])  # trg valve to pump
    #             port_2 = port_2_tuple[1]
    #             port_3 = port_3_tuple[1]
    #             # check volumes
    #             source_node = search.get_node_from_label("source")
    #             target_node = search.get_node_from_label("target")
    #             a = source_node.check_transfer(-volume)
    #             b = target_node.check_transfer(volume)
    #             if a and b:
    #                 if source_node["Removable"] and target_node["Addable"]:
    #                     node["object"].dispense(port_2, port_3, 1.0, volume, wait_ready)
    #                     # node["object"].move(port_2, 1, volume, wait_ready)
    #                     source_node.update_volume(-volume)
    #                     source_node.update_volume(volume)
    #                     print(f"{volume} was transferred to {port_3} from {port_2}")


def cli_main():
    graph_1_gen = Generator(GRAPH_JSON)
    graph_1 = graph_1_gen.generate_graph()
    search = GraphSearch(graph_1)

    transfer = Transfer(search, "sln_1", "rxn_1", 1.0)
    transfer()


if __name__ == "__main__":
    cli_main()
