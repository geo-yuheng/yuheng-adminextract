import networkx as nx

from localization import i18n_string


def prune_graph_to_root(G: nx.DiGraph, root_id: int) -> nx.DiGraph:
    """
    Modifies the graph G so that it only contains nodes that are reachable from the root node.
    This function first identifies all nodes that are reachable from the root node and then removes all unreachable nodes.

    Args:
        G (nx.DiGraph): The original graph.
        root_id (int): The ID of the root node.

    Returns:
        nx.DiGraph: The modified graph containing only nodes reachable from the root node.

    修改图G，使其只包含从根节点可达的节点。
    该函数首先识别所有从根节点可达的节点，然后移除所有不可达的节点。

    参数:
        G (nx.DiGraph): 原始图。
        root_id (int): 根节点的ID。

    返回:
        nx.DiGraph: 仅包含从根节点可达的节点的修改后的图。
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
    Prunes the graph G based on the stop_level and only_level parameters. If stop_level is provided, all nodes with
    a higher administrative level than stop_level are removed. If only_level is provided, only nodes with that
    specific administrative level are kept.

    Args:
        G (nx.DiGraph): The original graph.
        stop_level (int, optional): The administrative level to stop pruning at. Nodes with a higher level are removed. Defaults to None.
        only_level (int, optional): If set, only nodes of this specific administrative level are included. Defaults to None.

    Returns:
        nx.DiGraph: The pruned graph.

    根据 stop_level 和 only_level 参数修剪图G。如果提供了 stop_level，则移除所有高于 stop_level 的行政级别的节点。如果提供了 only_level，
    则只保留该特定行政级别的节点。

    参数:
        G (nx.DiGraph): 原始图。
        stop_level (int, 可选): 停止修剪的行政级别。高于此级别的节点将被移除。默认为 None。
        only_level (int, 可选): 如果设置，仅包括此特定行政级别的节点。默认为 None。     

    返回:
        nx.DiGraph: 被修剪后的图。
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
