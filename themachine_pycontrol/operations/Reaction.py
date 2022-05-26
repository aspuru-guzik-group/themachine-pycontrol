import pkg_resources
import networkx as nx
from themachine_pycontrol.graph import Generator, GraphSearch
from themachine_pycontrol.operations import LiquidTransfer, FlushTubes, HeatStir, AtmosphereController

GRAPH_JSON = pkg_resources.resource_filename(
    "themachine_pycontrol", "graph/graph.json"
)
class Reaction:
    """
    Defines a Reaction class that pertains to running a series of transfers for a set of reactions
    sharing the same wash solvent, temperature, and rpm.
    """

    def __init__(self, graph, transfers: list[dict], temp: int, rpm: int, wash_solvent: str, purge_minutes: int = 10):
        self.graph = graph
        self.search = GraphSearch(graph)
        self.transfers = transfers
        self.temp = temp
        self.rpm = rpm
        self.wash_solvent = wash_solvent
        self.purge_minutes = purge_minutes
        self.targets = []
        for step in self.transfers:
            self.targets.append(step["target"])

    def __call__(self):
        """
        When a Transfer object is called, ex: transfer_1(), the transfer_liquid() function is called.
        """
        self.full_rxn()

    def atmosphere(self):
        """
        Purges each target in self.transfers for purge_minutes, then sets constant atmosphere
        """
        for target in self.targets:
            atm_controller = AtmosphereController(self.search, target)
            atm_controller.timed_purge(self.purge_minutes)

    def set_all_hotplates(self):
        """
        Sets the heat and temperature for all hotplates identified as necessary to the reaction.
        """
        target_hotplates = []
        for target in self.targets:
            heatstir = HeatStir(self.search, target, self.temp, self.rpm)
            if heatstir.find_hotplate() in target_hotplates:
                pass
            else:
                target_hotplates.append(heatstir.find_hotplate())
                heatstir()

    def perform_transfer(self, source: str, target: str, volume: int, wash_solvent: str):
        """
        Performs a single transfer given a source, target, and volume
        """
        transfer = LiquidTransfer(self.search, source, target, volume)
        if transfer.path_dirty_tubes():
            transfer()
        else:
            flush = FlushTubes(self.search, wash_solvent, "waste", 0.5)
            flush()
            transfer()

    def perform_all_transfers(self):
        """
        Performs all transfers in self.transfers
        """
        for transfer in self.transfers:
            source = transfer["source"]
            target = transfer["target"]
            volume = transfer["volume"]
            self.perform_transfer(source, target, volume, self.wash_solvent)

    def full_rxn(self):
        """
        Sets atmosphere for all necessary vessels, performs all transfers while washing tubes as necessary
        with self.wash_solvent, then sets all hotplates as necessary.

        """
        self.atmosphere()
        self.perform_all_transfers()
        self.set_all_hotplates()



def main():


    graph_1_gen = Generator(GRAPH_JSON)
    graph_1 = graph_1_gen.generate_graph()



    #without reaction class:
    search = GraphSearch(graph_1)

    atmosphere_1 = AtmosphereController(search, "rxn_1")
    flush_1 = FlushTubes(search, "sln_3", "waste", 0.5)
    heatstir_1 = HeatStir(search, "rxn_1", 40, 120)

    transfer_1 = LiquidTransfer(search, "sln_1", "rxn_1", 1.0)
    transfer_2 = LiquidTransfer(search, "sln_2", "rxn_1", 2.0)
    transfer_3 = LiquidTransfer(search, "sln_3", "rxn_1", 5.0)


    atmosphere_1.timed_purge(10)

    transfer_1()
    transfer_2()
    transfer_3()

    flush_1.flush_dirty_tubes()

    heatstir_1()


    #with reaction class:


    test_rxn_transfers = [
        {
            "source": "sln_1",
            "target": "rxn_1",
            "volume": 1.0
        },
        {
            "source": "sln_2",
            "target": "rxn_1",
            "volume": 2.0
        }
    ]

    test_reaction = Reaction(graph_1, test_rxn_transfers, 40, 120, "sln_3")
    test_reaction()




if __name__ == "__main__":
    main()