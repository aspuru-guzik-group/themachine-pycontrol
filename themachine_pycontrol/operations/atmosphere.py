import pkg_resources

from themachine_pycontrol.graph.generator import Generator
from themachine_pycontrol.graph.search import GraphSearch

GRAPH_JSON = pkg_resources.resource_filename(
    "themachine_pycontrol", "graph/graph.json"
)


class AtmosphereController:  
    """
    Class that contains the functions for controlling the atmosphere of the vessels.

    === Public Attributes ==
    search: the GraphSearch object that will be used to perform graph search operations
    gas_path: the shortest path of nodes and edges from the gas source to the vessel
    waste_path: the shortest path of nodes and edges from the vessel to the waste
    gas_relay: the Relay objet in the gas_path
    waste_relay: the Relay object in the waste_path

    === Representation Invariants ===
    - the shortest path from a vessel to the gas source or to the waste must contain one relay object

    """
    def __init__(self, search: GraphSearch, vessel: str):
        """
        Instantiates a Transfer object.
        """
        self.search = search
        self.gas_path = self.search.path_search("N2", vessel)
        self.waste_path = self.search.path_search(vessel, "waste")
        self.gas_relay = self._find_gas_relay()
        self.waste_relay = self._find_waste_relay()

    def _find_gas_relay(self) -> Relay:
        """
        Returns the relay object in the path from the gas source to the specified vessel.
        """
        nodes, edges = self.gas_path
        for node in nodes:
            if node["class"] == "Relay":
                return node["object"]

    def _find_waste_relay(self) -> Relay:
        """
        Returns the relay object in the path from the specified vessel to the waste.
        """
        nodes, edges = self.waste_path
        for node in nodes:
            if node["class"] == "Relay":
                return node["object"]

    def exchange_atm(self):
        """
        Opens gasflow from the gas source to the vessel and from the vessel to the waste by switching the relay
        connecting the gas to the vessel and the relay from the vessel to the waste to True.
        """
        self.gas_relay.set_relay(True)
        self.waste_relay.set_relay(True)
        print(f"Relay {self.gas_relay.relay_num} and relay {self.waste_relay.relay_num} are both True/open.")

    def set_atm(self):
        """
        Keeps the vessel under constant inert atmosphere by enabling gasflow from the gas source to the vessel.
        No gasflow out of the vial is permitted.
        """
        self.gas_relay.set_relay(True)
        self.waste_relay.set_relay(False)
        print(f"Relay {self.gas_relay.relay_num} is True/open and relay {self.waste_relay.relay_num} is False/closed.")

    def timed_purge(self, purge_minutes: int):
        """
        Exchanges atmosphere (enables gas flow from the gas source to the vessel and then to the weaste) for the
        amount of time corresponding to purge_minutes, then maintains constant pressure from the gas source.
        """
        purge_seconds = purge_minutes*60
        self.exhange_atm
        self.sleep(purge_seconds)
        self.set_atm


def main():
    graph_1_gen = Generator(GRAPH_JSON)
    graph_1 = graph_1_gen.generate_graph()
    search = GraphSearch(graph_1)

    atm_1 = AtmosphereController(search, "rxn_1")
    atm_1.exchange_atm()


if __name__ == "__main__":
    main()
