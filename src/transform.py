from typing import Dict

import networkx as nx


def graph_to_nested_json(G: nx.DiGraph, root_id: int) -> Dict:
    """
    Converts a directed graph to a nested JSON structure starting from a specified root node.

    Args:
        G (nx.DiGraph): The directed graph to convert.
        root_id (int): The ID of the root node from which to start the nesting.

    Returns:
        Dict: A nested dictionary representing the hierarchical structure.

    将有向图转换为从指定根节点开始的嵌套 JSON 结构。

    参数:
        G (nx.DiGraph): 要转换的有向图。
        root_id (int): 开始嵌套的根节点的 ID。

    返回:
        Dict: 表示层级结构的嵌套字典。
    """

    def recurse(node):
        node_data = G.nodes[node]
        children = [recurse(child) for child in G.successors(node)]
        children = [child for child in children if child is not None]
        return {
            "id": node,
            **node_data,
            "subareas": children,
        }

    return recurse(root_id)


def graph_to_plain_json(G: nx.DiGraph, admin_level: int = None) -> Dict:
    """
    Converts a directed graph to a plain JSON structure, optionally filtering by admin level.

    Args:
        G (nx.DiGraph): The directed graph to convert.
        admin_level (int, optional): If set, only nodes of this administrative level are included. Defaults to None.

    Returns:
        Dict: A dictionary representing the nodes in a flat structure.
    """
    nodes = []
    for node, data in G.nodes(data=True):
        if (
            admin_level is None
            or int(data.get("admin_level", 0)) == admin_level
        ):
            nodes.append({"id": node, **data})
    return {"nodes": nodes}


def visualize_graph(
    G: nx.DiGraph,
    method: str = "gv",
    gv_filename: str = "graph.gv",
    show: bool = False,
) -> None:
    """
    Visualizes the directed graph using either matplotlib (plt) or Graphviz (gv).

    Args:
        G (nx.DiGraph): The directed graph to visualize.
        method (str): The visualization method to use ('plt' for matplotlib, 'gv' for Graphviz). Defaults to 'gv'.
        gv_filename (str): The filename for the generated Graphviz (.gv) file. Only relevant if method is 'gv'. Defaults to "graph.gv".
        show (bool): If True and method is 'plt', the graph will be visualized immediately. Defaults to False.
    """

    if method == "plt":
        if show:
            import matplotlib.pyplot as plt
            import networkx as nx
            from networkx.drawing.nx_agraph import graphviz_layout

            pos = graphviz_layout(G, prog="dot")
            sizes = [
                8000 / (int(G.nodes[node].get("admin_level") or 10) + 1)
                for node in G.nodes()
            ]
            nx.draw(G, pos, with_labels=True, node_size=sizes, arrows=True)
            plt.show()

    elif method == "gv":
        with open(gv_filename, "w", encoding="utf-8") as f:
            f.write("digraph G {\n")
            # Optional: Set graph, node, and edge attributes here
            # f.write('  node [shape=box];\n')  # Example node attribute
            for node in G.nodes():
                admin_level = G.nodes[node].get("admin_level", "N/A")
                name = G.nodes[node].get("name", "Unnamed")
                label = f"{admin_level}\\n{name}\\n{node}"
                f.write(f'  "{node}" [label="{label}"];\n')
            for edge in G.edges():
                f.write(f'  "{edge[0]}" -> "{edge[1]}";\n')
            f.write("}\n")

    else:
        raise ValueError("Invalid visualization method. Choose 'plt' or 'gv'.")
