from typing import Dict

import networkx as nx

from localization import i18n_string


def graph_to_nested_json(G: nx.DiGraph, root_id: int) -> Dict:
    """
    Converts a directed graph to a nested JSON structure starting from a specified root node.

    This function iterates over the graph starting from the root node, creating a hierarchical
    structure that represents the graph's topology as a nested dictionary. Each node in the
    dictionary contains an ID, any additional data stored in the node, and a list of its children.

    Args:
        G (nx.DiGraph): The directed graph to convert.
        root_id (int): The ID of the root node from which to start the nesting.

    Returns:
        Dict: A nested dictionary representing the hierarchical structure of the graph.

    将有向图转换为从指定根节点开始的嵌套 JSON 结构。

    该函数从根节点开始遍历图，创建一个表示图拓扑结构的层级字典结构。字典中的每个节点包含一个 ID、
    存储在节点中的任何附加数据以及其子节点的列表。

    参数:
        G (nx.DiGraph): 要转换的有向图。
        root_id (int): 开始嵌套的根节点的 ID。

    返回:
        Dict: 表示图的层级结构的嵌套字典。
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
    Converts a directed graph to a plain JSON structure, optionally filtering by administrative level.

    This function iterates over all nodes in the graph, optionally filtering them by administrative level,
    and then compiles a list of these nodes into a flat JSON structure. Each node in the list contains its ID
    and any associated data.

    Args:
        G (nx.DiGraph): The directed graph to convert.
        admin_level (int, optional): If set, only nodes of this administrative level are included. Defaults to None.

    Returns:
        Dict: A dictionary representing the nodes in a flat structure.

    将有向图转换为平面 JSON 结构，可选择按行政级别过滤。

    该函数遍历图中的所有节点，可选择按行政级别过滤，然后将这些节点编译成一个平面 JSON 结构的列表。列表中的每个节点包含其 ID 和任何关联的数据。

    参数:
        G (nx.DiGraph): 要转换的有向图。
        admin_level (int, 可选): 如果设置，只包括此行政级别的节点。默认为 None。

    返回:
        Dict: 以平面结构表示的节点的字典。
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

    This function supports two visualization methods: matplotlib for inline plotting and Graphviz for generating
    .gv files that can be further processed or viewed with Graphviz tools. The visualization method can be chosen
    with the 'method' parameter. For matplotlib, if 'show' is True, the graph will be displayed immediately.

    Args:
        G (nx.DiGraph): The directed graph to visualize.
        method (str): The visualization method to use ('plt' for matplotlib, 'gv' for Graphviz). Defaults to 'gv'.
        gv_filename (str): The filename for the generated Graphviz (.gv) file. Only relevant if method is 'gv'. Defaults to "graph.gv".
        show (bool): If True and method is 'plt', the graph will be visualized immediately. Defaults to False.

    使用 matplotlib (plt) 或 Graphviz (gv) 可视化有向图。

    该函数支持两种可视化方法：matplotlib 用于内联绘图，Graphviz 用于生成可以进一步处理或使用 Graphviz 工具查看的 .gv 文件。
    可使用 'method' 参数选择可视化方法。对于 matplotlib，如果 'show' 为 True，则图形将立即显示。

    参数:
        G (nx.DiGraph): 要可视化的有向图。
        method (str): 要使用的可视化方法（'plt' 用于 matplotlib，'gv' 用于 Graphviz）。 默认为 'gv'。
        gv_filename (str): 生成的 Graphviz (.gv) 文件的文件名。仅当方法为 'gv' 时相关。 默认为 "graph.gv"。
        show (bool): 如果为 True 且方法为 'plt'，则图形将立即可视化。默认为 False。
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
        raise ValueError(i18n_string("wrong-vis-method"))
