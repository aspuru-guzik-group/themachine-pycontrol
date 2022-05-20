import pkg_resources
# TODO: Same will __all__ for graph directory
from themachine_pycontrol.graph.generator import Generator
from themachine_pycontrol.graph.search import GraphSearch
from errors import HardwareError, RangeError

# TODO: .
GRAPH_JSON = pkg_resources.resource_filename(
    "themachine_pycontrol", "graph/graph.json"
)


class LiquidTransfer:
    """
    Class that contains the functions for transferring liquids across the graph representing the Machine.

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
        nodes, edges = path  # FIXME: Errors because where does path come from??
        self.move_liquid(self.draw_path, direction=True)
        self.move_liquid(self.dispense_path, direction=False)
        for node, next_node in zip(nodes[0:], nodes[1:]):
            # FIXME: Use any() instead of multiple or.
            # FIXME: "type" key should be in quotes!
            if node[type] == "stock_vial" or node[type] == "rxn_vial" or next_node[type] == "stock_vial" or next_node[type] == "rxn_vial":
                pass
            else:
                edge = self.search.edge_search(node["name"], next_node["name"])
                self._update_clean_state(False, edge)

    def move_liquid(self, path: tuple, direction: bool, volume=self.volume):
        # FIXME: volume shouldn't be an arg because it's always related to the LiquidTransfer instance.
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
                for edge in edges:  # can be improved with Path class
                    if edge["target"] == node["label"]:
                        valve_port = eval(edge["port_num"])[1]
                        node["object"].move(valve_port)

    def _pump_liquid(self, nodes: list, edges: list, direction: bool, volume):
        # FIXME: volume shouldn't be an arg because it's always related to the LiquidTransfer instance.
        """
        Draws (if direction is True) or dispenses (if direction is False) liquid of quantity volume via the path
        corresponding to the specified nodes and edges.
        """
        self._vessel_change(nodes, direction)
        for node in nodes:
            if node["class"] == "Pump":
                for edge in edges:  # can be improved with Path class
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
                if direction:  # TODO: I have so many questions about this...
                    if node["Removable"]:
                        if node["object"].check_transfer(self.volume):
                            node["object"].update_volume(self.volume)
                        else:
                            raise RangeError("This volume cannot be drawn")  # FIXME: These errors should be in Vessel (and more specific)
                    else:
                        raise Exception("This vessel cannot be drawn from")  # FIXME: These errors should be in Vessel (and more specific)
                else:
                    if node["Addable"]:
                        if node["object"].check_transfer(-self.volume):
                            node["object"].update_volume(-self.volume)
                        else:
                            raise HardwareError("This volume cannot be drawn")  # FIXME: These errors should be in Vessel (and more specific)
                    else:
                        raise HardwareError("This vessel cannot be drawn from")  # FIXME: These errors should be in Vessel (and more specific)

    def flush_dirty_tubes(self, wash_label: str, waste_label: str = "waste"):
        # TODO: This should be two methods: check_dirty_tubes() and have while check_dirty_tubes(): in flush_dirty_tubes()
        """
        Cleans all contaminated tubes with 2.0 mL of wash solvent.
        """
        all_edges = self.search.get_all_edge_data()
        for edge in all_edges:  # FIXME: edges won't be updated when you clean the tubes!
            edge_data = edge[2]
            if edge_data["clean"] == 0:  # Equivalent to clean == False
                # FIXME: dirty_path doesn't necessarily pass through edge!
                dirty_path = self.search.dirtiest_path("volumetric", wash_label, waste_label, self.common)
                self.move_liquid(dirty_path[0], direction=True, volume=2.0)  # FIXME: Don't hard-code this!
                self.move_liquid(dirty_path[1], direction=False, volume=2.0)  # FIXME: Don't hard-code this!
                self._update_clean_state(True, *dirty_path[0][1])
                self._update_clean_state(True, *dirty_path[1][1])
            else:
                print("All tubes are clean")

    # TODO: static method?
    def _update_clean_state(self, state: bool, *edges):  # TODO: Ask your nearest postdoc about *args
        for edge in edges:
            edge["clean"] = int(state)


def main():
    graph_1_gen = Generator(GRAPH_JSON)
    graph_1 = graph_1_gen.generate_graph()
    search = GraphSearch(graph_1)

    transfer = LiquidTransfer(search, "sln_1", "rxn_1", 1.0)
    # transfer()


if __name__ == "__main__":
    main()
