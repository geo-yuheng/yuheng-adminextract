import networkx as nx

from localization import i18n_string


def prune_graph_to_root(G: nx.DiGraph, root_id: int) -> nx.DiGraph:
    """
    修改图G，使其只包含与根节点联通的节点。
    这个函数首先找到所有从根节点可达的节点，然后移除所有不可达的节点。

    :param G: 原始图。
    :param root_id: 根节点的ID。
    :return: 修改后的图。
    """
    reachable = set(nx.descendants(G, root_id)) | {root_id}
    for node in list(G.nodes):
        if node not in reachable:
            G.remove_node(node)
    return G


def prune_graph_to_level(
    G: nx.DiGraph, stop_level: int = None, only_level: int = None
) -> nx.DiGraph:
    """
    Prunes the graph G based on the stop_level and only_level parameters.

    Args:
        G (nx.DiGraph): The original graph.
        stop_level (int, optional): The administrative level to stop pruning at. Defaults to None.
        only_level (int, optional): If set, only nodes of this administrative level are included. Defaults to None.

    Returns:
        nx.DiGraph: The pruned graph.
    """
    if stop_level is not None and only_level is not None:
        print(i18n_string("error_conflict"))

    nodes_to_remove = []
    for node, data in G.nodes(data=True):
        admin_level = data.get("admin_level")
        if admin_level is None:
            continue
        level = int(admin_level)
        if stop_level is not None and level > stop_level:
            nodes_to_remove.append(node)
        elif only_level is not None and level != only_level:
            nodes_to_remove.append(node)

    for node in nodes_to_remove:
        G.remove_node(node)

    return G
