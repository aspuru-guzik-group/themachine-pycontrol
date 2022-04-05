import pkg_resources
import pickle
# import networkx as nx
# import json
from themachine_pycontrol.drivers.vessel import Vessel
# from themachine_pycontrol.drivers.hotplate import Hotplate
from themachine_pycontrol.drivers.valve import Valve
from themachine_pycontrol.drivers.pump import Pump
from themachine_pycontrol.main.graph_search import GraphSearch
import typing

GRAPH_PKL = pkg_resources.resource_filename(
    "themachine_pycontrol", "graphgen/graph.pkl"
)


def transfer(graph_path, volume: int, source, target, wait_ready: bool):
    """
    Note: assumes source and target are rxn or sln vessels.
    """
    search = GraphSearch(graph_path)
    traversed_edges = search.multistep_edges(source, target)
    # for edge in traversed_edges:
    #     port_1_tuple = eval(edge[2]["port_num"])
    #     port_1 = port_1_tuple[1]
    #     search.get_node(edge[node["object"].move(port_1)
    traversed_nodes: list = search.multistep_search(source, target)
    for node in traversed_nodes:
        if node["label"] == traversed_nodes[0]:
            # edge_1 = search.edge_search(search.edge_search(source, node["label"]))
            edge_1 = traversed_edges[0]
            port_1_tuple = eval(edge_1[2]["port_num"])
            port_1 = port_1_tuple[1]
            node["object"].move(port_1)
            print(f"{traversed_nodes[0]} has been opened to port {port_1}.")
        elif node["label"] == traversed_nodes[2]:
            edge_4 = traversed_edges[3]
            port_4_tuple = eval(edge_4[2]["port_num"])
            port_4 = port_4_tuple[1]
            node["object"].move(port_4)
            print(f"{traversed_nodes[2]} has been opened to port {port_4}.")
        elif node["label"] == traversed_nodes[1]:
            edge_2 = traversed_edges[1]
            edge_3 = traversed_edges[2]
            port_2_tuple = eval(edge_2[2]["port_num"])  # src valve to pump
            port_3_tuple = eval(edge_3[2]["port_num"])  # trg valve to pump
            port_2 = port_2_tuple[1]
            port_3 = port_3_tuple[1]
            # check volumes
            source_node = search.get_node_from_label("source")
            target_node = search.get_node_from_label("target")
            a = source_node.check_transfer(-volume)
            b = target_node.check_transfer(volume)
            if a and b:
                if source_node["Removable"] and target_node["Addable"]:
                    node["object"].dispense(port_2, port_3, 1.0, volume, wait_ready)
                    # node["object"].move(port_2, 1, volume, wait_ready)
                    source_node.update_volume(-volume)
                    source_node.update_volume(volume)
                    print(f"{volume} was transferred to {port_3} from {port_2}")


def heat(graph_path, object_label, temp):
    """

    """
    search = GraphSearch(graph_path)
    hotplate = search.single_search(object_label, False)
    print(hotplate)
    hotplate["object"].heat(True, temp)


def stir(graph_path, object_label, rpm):
    """

    """
    search = GraphSearch(graph_path)
    hotplate = search.single_search(object_label, False)
    hotplate["object"].stir(True, rpm)


def cli_main():
    graph_1 = GraphSearch(GRAPH_PKL)
    transfer(graph_1, 10, "sln_1", "rxn_1", True)
    # heat(graph_1, "rxn_12,", 20)


if __name__ == "__main__":
    cli_main()
