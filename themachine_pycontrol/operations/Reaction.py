import pkg_resources
import networkx as nx
from themachine_pycontrol.graph import Generator, GraphSearch
from themachine_pycontrol.operations import LiquidTransfer, FlushTubes, HeatStir, AtmosphereController

GRAPH_JSON = pkg_resources.resource_filename(
    "themachine_pycontrol", "graph/graph.json"
)



def main():
    graph_1_gen = Generator(GRAPH_JSON)
    graph_1 = graph_1_gen.generate_graph()
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



if __name__ == "__main__":
    main()