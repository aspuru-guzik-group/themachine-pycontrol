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
        self.draw_path, self.dispense_path = self.search.multistep_search(source, target, self.common)
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
        self.move_liquid(self.draw_path, direction=True)
        self.move_liquid(self.dispense_path, direction=False)

    def move_liquid(self, path: tuple, direction: bool):
        """
        Draws or dispenses liquid of specified volume from an object using the pump,
        setting intermediary valves to the correct positions to facilitate this transfer
        """
        nodes, edges = path
        self._set_valves(nodes, edges)
        self._pump_liquid(nodes, edges, direction)

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

    def _pump_liquid(self, nodes: list, edges: list, direction: bool):
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
                            node["object"].move(pump_port, 25, self.volume)
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
                            raise Exception("This volume cannot be drawn")
                    else:
                        raise Exception("This vessel cannot be drawn from")
                else:
                    if node["Addable"]:
                        if node["object"].check_transfer(-self.volume):
                            node["object"].update_volume(-self.volume
                        else:
                            raise Exception("This volume cannot be drawn")
                    else:
                        raise Exception("This vessel cannot be drawn from")



def cli_main():
    graph_1_gen = Generator(GRAPH_JSON)
    graph_1 = graph_1_gen.generate_graph()
    search = GraphSearch(graph_1)

    transfer = Transfer(search, "sln_1", "rxn_1", 1.0)
    transfer()


if __name__ == "__main__":
    cli_main()
