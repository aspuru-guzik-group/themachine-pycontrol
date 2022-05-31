import pkg_resources
import networkx as nx
from themachine_pycontrol.graph import Generator, GraphSearch

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
        self.draw_path, self.dispense_path = self.search.specific_multistep_search("volumetric", source, target,
                                                                                   nx.shortest_path, self.common)
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
        draw_nodes, draw_edges = self.draw_path
        dispense_nodes, dispense_edges = self.dispense_path
        paths = [draw_nodes, dispense_nodes]
        self.move_liquid(self.draw_path, direction=True, volume=self.volume)
        self.move_liquid(self.dispense_path, direction=False, volume=self.volume)
        for nodes in paths:
            print(nodes)
            for node, next_node in zip(nodes[0:], nodes[1:]):
                incontaminable_edges = [
                    node["type"] == "stock_vial",
                    node["type"] == "rxn_vial",
                    next_node["type"] == "stock_vial",
                    next_node["type"] == "rxn_vial",
                    next_node["type"] == "waste"
                ]
                incontaminable = any(incontaminable_edges)
                if incontaminable:
                    continue
                else:
                    edge = self.search.graph.get_edge_data(node["id"], next_node["id"])
                    self._update_clean_state(False, edge)

    def move_liquid(self, path: tuple, direction: bool, volume: float):
        """
        Draws or dispenses liquid of specified volume from an object using the pump,
        setting intermediary valves to the correct positions to facilitate this transfer
        """
        # self.volume wouldnt work as argument? couldnt find self
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
        """
        Draws (if direction is True) or dispenses (if direction is False) liquid of quantity volume via the path
        corresponding to the specified nodes and edges.
        """
        self._vessel_change(nodes, direction)
        for node in nodes:
            if node["class"] == "Pump":
                for edge in edges:  # can be improved with Path class
                    if edge["target"] == node["label"]:
                        port_num = eval(edge["port_num"])
                        pump_port = port_num[1]
                        # pump_port = eval(edge["port_num"][1]))
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
                    node["object"].update_volume(self.volume, direction)
                else:
                    node["object"].update_volume(self.volume, direction)

    @staticmethod
    def _update_clean_state(state: bool, *edges):
        for edge in edges:
            edge["clean"] = int(state)
            print(edge["clean"])

    def path_dirty_tubes(self):
        """
        """
        edges = [edge for edge in self.draw_path[1] and self.dispense_path[1]]
        for edge in edges:
            edge_data = edge[2]
            return edge_data["clean"]


class FlushTubes(LiquidTransfer):
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

    def __init__(self, search: GraphSearch, wash_label: str, waste_label: str, flush_volume: float):
        super().__init__(search, wash_label, waste_label, flush_volume)
        self.wash_label = wash_label
        self.common = "pump_1"
        self.search = search
        self.flush_volume = flush_volume
        self.dirty_path = self.search.dirtiest_path("volumetric", wash_label, waste_label, self.common)

    def __call__(self):
        """
        When a FlushTubes object is called, ex: flushtubes_1(), the flush_dirty_tubes() function is called.
        """
        self.flush_dirty_tubes(self.flush_volume)

    def check_dirty_tubes(self):
        """
        Returns the "clean" attribute for all edges in the graph, giving True if the edge is clean and False
        if the edge is dirty.
        """
        all_edges = self.search.get_all_edge_data()
        for edge in all_edges:  # FIXME: edges won't be updated when you clean the tubes!
            edge_data = edge[2]
            clean = edge_data["clean"]
            print(clean)
            try:
                if clean >= 1:
                    continue
                else:
                    return False
            except TypeError:
                continue
        return True

    def flush_dirty_tubes(self, flush_vol: float = 0.5):
        """
        Cleans all contaminated tubes with 2.0 mL of wash solvent.
        """
        while not self.check_dirty_tubes():
            # FIXME: dirty_path doesn't necessarily pass through edge!
            # ^ Is this a problem? Purpose is to re-do the search as long as any edge is dirty

            a = self.dirty_path[0]
            b = self.dirty_path[1]

            self.move_liquid(self.dirty_path[0], direction=True, volume=flush_vol)
            self.move_liquid(self.dirty_path[1], direction=False, volume=flush_vol)

            c = self.dirty_path[0][1]
            d = self.dirty_path[1][1]
            self._update_clean_state(True, *self.dirty_path[0][1])
            self._update_clean_state(True, *self.dirty_path[1][1])
            print("check")
            print(self.check_dirty_tubes())
        print("All tubes are clean")


def main():
    graph_1_gen = Generator(GRAPH_JSON)
    graph_1 = graph_1_gen.generate_graph()
    search = GraphSearch(graph_1)

    transfer = LiquidTransfer(search, "sln_1", "rxn_1", 1.0)
    transfer1 = LiquidTransfer(search, "sln_3", "rxn_10", 1.0)
    flush = FlushTubes(search, "sln_2", "waste", 0.5)
    transfer1()

    #print(flush.check_dirty_tubes())
    flush.flush_dirty_tubes()


if __name__ == "__main__":
    main()
