import pkg_resources

import networkx as nx
import json
from themachine_pycontrol.drivers.vessel import Vessel
from themachine_pycontrol.drivers.hotplate import Hotplate
from themachine_pycontrol.drivers.valve import Valve
from themachine_pycontrol.graphgen.generator import Generator
from themachine_pycontrol.drivers.pump import Pump
from themachine_pycontrol.main.graph_search import GraphSearch
from errors import CommunicationError, HardwareError, RangeError
import typing

GRAPH_JSON = pkg_resources.resource_filename(
    "themachine_pycontrol", "graphgen/graph.json"
)

class Transfer:
    """
    Class that contains the functions for transferring liqids across the graph representing the Machine.

    === Public Attributes ==
    search: the GraphSearch object that will be used to perform graph search operations
    source: the label corresponding to the source node for the transfer
    target: the label corresponding to the target node for the transfer
    volume: the volume of liquid to be transferred

    === Representation Invariants ===
    - source and target must correspond to nodes featuring objects of the vessel class

    """
    def __init__(self, search: GraphSearch, source: str, target: str, volume: float):
        """
        Instantiates a Transfer object.
        """
        self.common = "pump_1"  # Hard-coded for now...
        self.search = search
        self.draw_path, self.dispense_path = self.search.specific_multistep_search("volumetric", source, target, self.common)
        self.volume = volume

    def __call__(self):
        """
        When a Transfer object is called, ex: transfer_1(), the transfer_liquid() function is called.
        """
        self.transfer_liquid()

    def transfer_liquid(self) -> None:
        """
        Draws liquid corresponding to volume from the source node object and dispenses it into the target node object.
        """
        nodes, edges = path
        self.move_liquid(self.draw_path, direction=True)
        self.move_liquid(self.dispense_path, direction=False)
        for node, next_node in zip(nodes[0:], nodes[1:]):
            if node[type] == "stock_vial" or node[type] == "rxn_vial" or next_node[type] == "stock_vial" or next_node[type] == "rxn_vial":
                pass
            else:
                edge = self.search.edge_search(node["name"], next_node["name"])
                self._update_contam(edge, False)

    def move_liquid(self, path: tuple, direction: bool, volume=self.volume):
        """
        Draws or dispenses liquid of specified volume from an object using the pump,
        setting intermediary valves to the correct positions to facilitate this transfer
        """
        nodes, edges = path
        self._set_valves(nodes, edges)
        self._pump_liquid(nodes, edges, direction, volume)

    def _set_valves(self, nodes: list, edges: list):
        """
        Sets all intermediary valves in place for a given path with the specified nodes and edges to enable a solution
        transfer.
        """
        for node in nodes:
            if node["class"] == "Valve":
                for edge in edges: #can be improved with Path class
                    if edge["target"] == node["label"]:
                        valve_port = eval(edge["port_num"])[1]
                        node["object"].move(valve_port)

    def _pump_liquid(self, nodes: list, edges: list, direction: bool, volume):
        """
        Draws (if direction is True) or dispenses (if direction is False) liquid of quantity volume via the path
        corresponding to the specified nodes and edges.
        """
        self._vessel_change(nodes, direction)
        for node in nodes:
            if node["class"] == "Pump":
                for edge in edges: #can be improved with Path class
                    if edge["target"] == node["label"]:
                        pump_port = edge["port_num"][1]
                        if direction:
                            node["object"].move(pump_port, 25, volume)
                        else:
                            node["object"].move(pump_port, 25, 0)

    def _vessel_change(self, nodes, direction):
        """
        Verifies if the transfer specified is possible given the vessel's volume specifications (max, min, and
        current volume), and if the vessel allows the addition or removal of liquid.
        If the transfer is allowed possible, the vessel's current_volume parameter is updated accordingly.
        """
        for node in nodes:
            if node["class"] == "Vessel":
                if direction:
                    if node["Removable"]:
                        if node["object"].check_transfer(self.volume):
                            node["object"].update_volume(self.volume)
                        else:
                            raise RangeError("This volume cannot be drawn")
                    else:
                        raise Exception("This vessel cannot be drawn from")
                else:
                    if node["Addable"]:
                        if node["object"].check_transfer(-self.volume):
                            node["object"].update_volume(-self.volume)
                        else:
                            raise HardwareError("This volume cannot be drawn")
                    else:
                        raise HardwareError("This vessel cannot be drawn from")

    def flush_dirty_tubes(self, wash_label: str, waste_label: str = "waste"):
        """
        Cleans all contaminated tubes with 2.0 mL of wash solvent.
        """
        all_edges = self.search.get_all_edge_data()
        for edge in all_edges:
            edge_data = edge[2]
            if edge_data["clean"] == 0:
                dirty_path = self.search.dirtiest_path("volumetric", wash_label, waste_label, self.common)
                self.move_liquid(dirty_path[0], direction=True, volume=2.0)
                self.move_liquid(dirty_path[1], direction=False, volume=2.0)
                self._update_multiple_contam(dirty_path[0][1], True)
                self._update_multiple_contam(dirty_path[1][1], True)
            else:
                print("All tubes are clean")

    def _update_contam(self, edge, clean_status: Bool):
        clean = int(clean_status)
        edge["clean"] = clean

    def _update_multiple_contam(self, edges, clean_status: Bool):
        clean = int(clean_status)
        for edge in edges:
            edge["clean"] = clean




def cli_main():
    graph_1_gen = Generator(GRAPH_JSON)
    graph_1 = graph_1_gen.generate_graph()
    search = GraphSearch(graph_1)

    transfer = Transfer(search, "sln_1", "rxn_1", 1.0)
    # transfer()


if __name__ == "__main__":
    cli_main()
