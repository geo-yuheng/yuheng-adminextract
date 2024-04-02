import argparse
import json
import os

import networkx as nx
from yuheng import Carto

from method.localization import i18n_string
from method.prune import prune_graph_to_level, prune_graph_to_root
from method.transform import (
    graph_to_nested_json,
    graph_to_plain_json,
    visualize_graph,
)


def build_graph(world: Carto) -> nx.DiGraph:
    """Constructs a directed graph from map data.

    Each administrative boundary from the map is added as a node, and subarea relationships are added as edges.

    Args:
        world: An instance of Carto containing map data.

    Returns:
        A directed graph representing the administrative hierarchy.

    根据地图数据构建有向图。

    地图中的每个行政边界都作为一个节点添加，子区域关系作为边缘添加。

    参数:
        world: 包含地图数据的 Carto 实例。

    返回:
        表示行政层级的有向图。
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
    """Finds the ID of the root node based on the given strategy.

    Args:
        G: The directed graph from which to find the root node.
        strategy: The strategy to use for finding the root node. Options are "input", "highest", "auto".

    Returns:
        The ID of the found root node.

    Raises:
        ValueError: If no root node can be found based on the given strategy.

    根据给定策略找到根节点的 ID。

    参数:
        G: 用于查找根节点的有向图。
        strategy: 用于查找根节点的策略。选项包括 "input"、"highest"、"auto"。

    返回:
        找到的根节点的 ID。

    异常:
        ValueError: 如果根据给定策略找不到根节点。
    """

    if strategy == "input":
        return int(input(i18n_string("prompt.find_root_node_id.root_node_id")))

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
            raise ValueError(
                i18n_string("error.find_root_node_id.no_root_node_found")
            )
        elif strategy == "auto":
            return int(
                input(
                    i18n_string("prompt.find_root_node_id.manual_root_node_id")
                )
            )

    if len(root_candidates) > 1:
        print(i18n_string("prompt.find_root_node_id.multiple_root_nodes"))
        for idx, (node, data) in enumerate(root_candidates):
            print(
                f"({idx + 1}). ID: [{node}], \"admin_level\": {data['admin_level']}, \"name\": {data.get('name')}, \"ref\": {data.get('ref')}"
            )

        node_ids = [node for node, _ in root_candidates]
        while True:
            try:
                input_id = int(
                    input(i18n_string("prompt.find_root_node_id.root_node_id"))
                )
                if input_id in node_ids:
                    return input_id
                else:
                    print(
                        i18n_string(
                            "error.find_root_node_id.error_invalid_node_id"
                        )
                    )
            except ValueError:
                print(
                    i18n_string("error.find_root_node_id.error_invalid_number")
                )

    return root_candidates[0][0]


def main():
    """Processes map data and outputs it as JSON or Graphviz file.

    This function accepts command line arguments to specify input and output file paths,
    output format, stop level, only level, connection enforcement, export format, and
    the strategy for root node selection.

    Args:
        --input-file: str, Path to the input map file. Defaults to 'map.osm'.
        --output-file: str, Path to the output file, either JSON or Graphviz format. Defaults to 'map.json'.
        --output-format: str, Specifies the output format. Choices are 'json' or 'gv'. Defaults to 'json'.
        --json-schema: str, Specifies the JSON schema format. Choices are 'nest' or 'plain'. Defaults to 'nest'.
        --stop-level: int, Specifies the stop level for processing. Incompatible with --only-level.
        --only-level: int, Specifies a single level to include in the output. Incompatible with --stop-level.
        --ensure-connected: bool, If set, ensures all nodes are connected to the root node. Not set by default.
        --root-select-strategy: str, Strategy to select the root node. Defaults to 'auto'.

    主要功能是读取地图数据，构建图结构，并根据指定的参数输出 JSON 文件或 Graphviz 文件。

    接受的命令行参数用于指定输入文件路径、输出文件路径、输出格式、停止级别、仅包含级别、
    是否确保所有节点与根节点相连、JSON模式（嵌套或平铺），以及选择根节点的策略。

    参数:
        --input-file: str, 输入地图文件的路径。默认为 'map.osm'。
        --output-file: str, 输出文件的路径，可以是 JSON 格式或 Graphviz 格式。默认为 'map.json'。
        --output-format: str, 指定输出格式。选项为 'json' 或 'gv'。默认为 'json'.
        --json-schema: str, 指定JSON架构格式。选项为 'nest' 或 'plain'。默认为 'nest'。
        --stop-level: int, 指定处理的停止级别。与 --only-level 不兼容。
        --only-level: int, 指定要在输出中仅包含的级别。与 --stop-level 不兼容。
        --ensure-connected: bool, 如果设置，确保所有节点都与根节点相连。默认未设置。
        --root-select-strategy: str, 选择根节点的策略。默认为 'auto'。
    """
    parser = argparse.ArgumentParser(
        description=i18n_string("description.main.app_function")
    )
    parser.add_argument(
        "--input-file",
        type=str,
        default="map.osm",
        help=i18n_string("help.main.input_file"),
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default="map.json",
        help=i18n_string("help.main.output_file"),
    )
    parser.add_argument(
        "--output-format",
        type=str,
        default="json",
        choices=["json", "gv"],
        help=i18n_string("help.main.output_format"),
    )

    parser.add_argument(
        "--json-schema",
        type=str,
        default="nest",
        choices=["nest", "plain"],
        help=i18n_string("help.main.json_schema"),
    )
    parser.add_argument(
        "--stop-level", type=int, help=i18n_string("help.main.stop_level")
    )
    parser.add_argument(
        "--only-level", type=int, help=i18n_string("help.main.only_level")
    )
    parser.add_argument(
        "--ensure-connected",
        action="store_true",
        help=i18n_string("help.main.ensure_connected"),
    )
    parser.add_argument(
        "--root-select-strategy",
        type=str,
        default="auto",
        help=i18n_string("help.main.root_select_strategy"),
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
            if args.json_schema == "plain":
                if args.only_level:
                    spec_level = args.only_level
                else:
                    spec_level = None
                json_output = json.dumps(
                    graph_to_plain_json(G, spec_level),
                    indent=2,
                    ensure_ascii=False,
                )
            else:  # args.json_schema == "nest"
                json_output = json.dumps(
                    graph_to_nested_json(G, root_id),
                    indent=2,
                    ensure_ascii=False,
                )
            with open(args.output_file, "w", encoding="utf-8") as f:
                f.write(json_output)
                print(
                    i18n_string("message.main.json_output_written").format(
                        output_file=args.output_file
                    )
                )
        except Exception as e:
            print(e)
    elif args.output_format == "gv":
        output_file_name = (
            os.path.splitext(args.output_file)[0] + ".gv"
            if os.path.splitext(args.output_file)[1].lower() == ".json"
            else args.output_file
        )
        visualize_graph(G, method="gv", gv_filename=output_file_name)


if __name__ == "__main__":
    main()
