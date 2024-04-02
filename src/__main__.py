import argparse
import json

import networkx as nx
from yuheng import Carto

from localization import i18n_string
from prune import prune_graph_to_level, prune_graph_to_root
from transform import (
    graph_to_nested_json,
    graph_to_plain_json,
    visualize_graph,
)


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

    world = Carto()
    world.read(mode="file", file_path=args.input_file)
    G = build_graph(world)

    print("args.output_format =", args.output_format)

    root_id = find_root_node_id(G, args.root_select_strategy)

    if args.ensure_connected:
        G = prune_graph_to_root(G, root_id)
    if args.stop_level is not None or args.only_level is not None:
        G = prune_graph_to_level(G, args.stop_level, args.only_level)

    if args.output_format == "json":
        try:
            if args.export_plain_json:
                json_output = json.dumps(
                    graph_to_plain_json(G, args.only_level),
                    indent=2,
                    ensure_ascii=False,
                )
            else:
                json_output = json.dumps(
                    graph_to_nested_json(G, root_id, args.stop_level, args.only_level),
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
