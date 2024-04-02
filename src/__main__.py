import networkx as nx
import json
import argparse
from typing import Dict
from yuheng import Carto

LOCALE = "zh"


def i18n_string(strid: str) -> str:
    """
    Returns localized strings based on the given string ID.

    Args:
        strid (str): A string identifier for the desired text.

    Returns:
        str: A localized string corresponding to the given ID.

    根据给定的字符串 ID 返回本地化字符串。

    参数:
        strid (str): 所需文本的字符串标识符。

    返回:
        str: 与给定 ID 对应的本地化字符串。
    """

    strings = {
        "en": {
            "enter-root-id": "Please enter the root node ID:",
            "no-root-found": "Unable to find root node ID, please ensure the graph contains administrative boundary nodes.",
            "enter-manual-root-id": "Unable to automatically determine the root node ID, please enter manually:",
            "invalid-id": "The entered ID is invalid, please enter a valid node ID.",
            "enter-valid-number": "Please enter a valid number.",
            "multiple-root-nodes": "Multiple root nodes of the same highest level found, please choose one as the root node:",
            "input_file_help": "Path to the input map file.",
            "output_file_help": "Path to the output JSON file.",
            "stop_level_help": "Set the desired stop level. Cannot be used with --only-level.",
            "only_level_help": "Set the level to exclusively include. Cannot be used with --stop-level.",
            "export_plain_json_help": "Export plain JSON instead of nested JSON.",
            "root_select_strategy_help": "Strategy to select the root node. Default is 'auto'.",
            "description": "Process map data and output JSON.",
            "error_conflict": "Error: STOP_LEVEL and ONLY_LEVEL cannot both be set.",
            "json_output": "JSON output has been written to {output_file}.",
        },
        "zh": {
            "enter-root-id": "请输入根节点ID：",
            "no-root-found": "无法找到根节点ID，请确保图中包含行政边界节点。",
            "enter-manual-root-id": "无法自动确定根节点ID，请手动输入：",
            "invalid-id": "输入的ID无效，请输入有效的节点ID。",
            "enter-valid-number": "请输入一个有效的数字。",
            "multiple-root-nodes": "发现多个同等最高级别的节点，请选择一个作为根节点：",
            "input_file_help": "输入地图文件的路径。",
            "output_file_help": "输出JSON文件的路径。",
            "stop_level_help": "设置所需的终止级别。不能与--only-level一起使用。",
            "only_level_help": "设置仅包含的级别。不能与--stop-level一起使用。",
            "export_plain_json_help": "导出普通JSON而不是嵌套JSON。",
            "root_select_strategy_help": "选择根节点的策略。默认为'auto'。",
            "description": "处理地图数据并输出JSON。",
            "error_conflict": "错误：STOP_LEVEL和ONLY_LEVEL不能同时设置。",
            "json_output": "JSON输出已写入{output_file}。",
        },
    }
    return strings.get(LOCALE, {}).get(strid, "")


def build_graph(world: Carto) -> nx.DiGraph:
    """
    Constructs a directed graph from map data.

    Each administrative boundary from the map is added as a node, and subarea relationships are added as edges.

    Args:
        world (Carto): An instance of Carto containing map data.

    Returns:
        nx.DiGraph: A directed graph representing the administrative hierarchy.

    根据地图数据构建有向图。

    地图中的每个行政边界都作为一个节点添加，子区域关系作为边缘添加。

    参数:
        world (Carto): 包含地图数据的 Carto 实例。

    返回:
        nx.DiGraph: 表示行政层级的有向图。
    """

    G = nx.DiGraph()
    for id, relation in world.relation_dict.items():
        admin_level = relation.tags.get("admin_level")
        name = relation.tags.get("name")
        ref = relation.tags.get("ref")
        if (
            "boundary" in relation.tags
            and relation.tags["boundary"] == "administrative"
        ):
            G.add_node(id, admin_level=admin_level, name=name, ref=ref)
            for member in relation.members:
                if (
                    member.role == "subarea"
                    and member.ref in world.relation_dict
                ):
                    G.add_edge(id, member.ref)
    return G


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


def find_root_node_id(G: nx.DiGraph, strategy="input") -> int:
    """
    Finds the ID of the root node based on the given strategy.

    Args:
        G (nx.DiGraph): The directed graph from which to find the root node.
        strategy (str): The strategy to use for finding the root node. Options are "input", "highest", "auto".

    Returns:
        int: The ID of the found root node.

    Raises:
        ValueError: If no root node can be found based on the given strategy.

    根据给定策略找到根节点的 ID。

    参数:
        G (nx.DiGraph): 用于查找根节点的有向图。
        strategy (str): 用于查找根节点的策略。选项包括 "input"、"highest"、"auto"。

    返回:
        int: 找到的根节点的 ID。

    引发:
        ValueError: 如果根据给定策略找不到根节点。
    """

    if strategy == "input":
        return int(input(i18n_string("enter-root-id")))

    min_level = float("inf")
    root_candidates = []
    for node, data in G.nodes(data=True):
        admin_level = data.get("admin_level")
        if admin_level is None:
            continue
        try:
            level = int(admin_level)
            if level < min_level:
                min_level = level
                root_candidates = [(node, data)]
            elif level == min_level:
                root_candidates.append((node, data))
        except ValueError:
            continue

    if not root_candidates:
        if strategy == "highest":
            raise ValueError(i18n_string("no-root-found"))
        elif strategy == "auto":
            return int(input(i18n_string("enter-manual-root-id")))

    if len(root_candidates) > 1:
        print(i18n_string("multiple-root-nodes"))
        for idx, (node, data) in enumerate(root_candidates):
            print(
                f"({idx + 1}). ID: [{node}], \"admin_level\": {data['admin_level']}, \"name\": {data.get('name')}, \"ref\": {data.get('ref')}"
            )

        node_ids = [node for node, _ in root_candidates]
        while True:
            try:
                input_id = int(input(i18n_string("enter-root-id")))
                if input_id in node_ids:
                    return input_id
                else:
                    print(i18n_string("invalid-id"))
            except ValueError:
                print(i18n_string("enter-valid-number"))

    return root_candidates[0][0]


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


def main():
    """
    Main function to process map data and output JSON.

    Accepts command line arguments for input and output file paths, stop level, only level,
    whether to export plain JSON, and the strategy to select the root node.

    - `--input-file`: Path to the input map file. Default is 'map.osm'.
    - `--output-file`: Path to the output JSON file. Default is 'map.json'.
    - `--stop-level`: Set the desired stop level. Cannot be used with --only-level.
    - `--only-level`: Set the level to exclusively include. Cannot be used with --stop-level.
    - `--export-plain-json`: Export plain JSON instead of nested JSON.
    - `--root-select-strategy`: Strategy to select the root node. Default is 'auto'.

    主函数用于读取地图数据，构建图结构，并输出 JSON 文件。

    接受命令行参数，用于指定输入文件路径、输出文件路径、停止级别、仅包含级别、
    是否导出无层级的JSON，以及选择根节点的策略。

    - `--input-file`：输入地图文件的路径。默认为 'map.osm'。
    - `--output-file`：输出 JSON 文件的路径。默认为 'map.json'。
    - `--stop-level`：设置期望的停止级别。不能与 --only-level 同时使用。
    - `--only-level`：设置要独家包含的级别。不能与 --stop-level 同时使用。
    - `--export-plain-json`：导出无层级的JSON 而不是嵌套 JSON。
    - `--root-select-strategy`：选择根节点的策略。默认为 'auto'。
    """
    parser = argparse.ArgumentParser(description=i18n_string("description"))
    parser.add_argument(
        "--input-file",
        type=str,
        default="map.osm",
        help=i18n_string("input_file_help"),
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default="map.json",
        help=i18n_string("output_file_help"),
    )
    parser.add_argument(
        "--output-format",
        type=str,
        default="json",
        choices=["json", "gv"],
        help="Output format: json or gv.",
    )
    parser.add_argument(
        "--stop-level", type=int, help=i18n_string("stop_level_help")
    )
    parser.add_argument(
        "--only-level", type=int, help=i18n_string("only_level_help")
    )
    parser.add_argument(
        "--ensure-connected",
        action="store_true",
        help="Ensure all nodes are connected to the root node.",
    )
    parser.add_argument(
        "--root-select-strategy",
        type=str,
        default="auto",
        help=i18n_string("root_select_strategy_help"),
    )
    parser.add_argument(
        "--export-plain-json",
        action="store_true",
        help=i18n_string("export_plain_json_help"),
    )
    args = parser.parse_args()

    STOP_LEVEL = args.stop_level
    ONLY_LEVEL = args.only_level
    EXPORT_PLAIN_JSON = args.export_plain_json
    ROOT_SELECT_STRATEGY = args.root_select_strategy

    world = Carto()
    world.read(mode="file", file_path=args.input_file)
    G = build_graph(world)

    print("args.output_format =", args.output_format)

    root_id = find_root_node_id(G, ROOT_SELECT_STRATEGY)
    if args.ensure_connected:
        G = prune_graph_to_root(G, root_id)
    if STOP_LEVEL is not None or ONLY_LEVEL is not None:
        G = prune_graph_to_level(G, STOP_LEVEL, ONLY_LEVEL)

    if args.output_format == "json":
        try:
            if EXPORT_PLAIN_JSON:
                json_output = json.dumps(
                    graph_to_plain_json(G, ONLY_LEVEL),
                    indent=2,
                    ensure_ascii=False,
                )
            else:
                json_output = json.dumps(
                    graph_to_nested_json(G, root_id, STOP_LEVEL, ONLY_LEVEL),
                    indent=2,
                    ensure_ascii=False,
                )
            with open(args.output_file, "w", encoding="utf-8") as f:
                f.write(json_output)
                print(
                    i18n_string("json_output").format(
                        output_file=args.output_file
                    )
                )
        except Exception as e:
            print(e)
    elif args.output_format == "gv":
        visualize_graph(G, method="gv", gv_filename="my_graph.gv")


if __name__ == "__main__":
    main()
