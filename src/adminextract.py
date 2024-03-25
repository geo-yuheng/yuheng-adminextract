import networkx as nx
import json
from typing import Dict
from kqs.waifu import Waifu

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
        },
        "zh": {
            "enter-root-id": "请输入根节点ID：",
            "no-root-found": "无法找到根节点ID，请确保图中包含行政边界节点。",
            "enter-manual-root-id": "无法自动确定根节点ID，请手动输入：",
            "invalid-id": "输入的ID无效，请输入有效的节点ID。",
            "enter-valid-number": "请输入一个有效的数字。",
            "multiple-root-nodes": "发现多个同等最高级别的节点，请选择一个作为根节点：",
        },
    }
    return strings.get(LOCALE, {}).get(strid, "")


def build_graph(map: Waifu) -> nx.DiGraph:
    """
    Constructs a directed graph from map data.

    Each administrative boundary from the map is added as a node, and subarea relationships are added as edges.

    Args:
        map (Waifu): An instance of Waifu containing map data.

    Returns:
        nx.DiGraph: A directed graph representing the administrative hierarchy.

    根据地图数据构建有向图。

    地图中的每个行政边界都作为一个节点添加，子区域关系作为边缘添加。

    参数:
        map (Waifu): 包含地图数据的 Waifu 实例。

    返回:
        nx.DiGraph: 表示行政层级的有向图。
    """

    G = nx.DiGraph()
    for id, relation in map.relation_dict.items():
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
                    and member.ref in map.relation_dict
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
        children = list(G.successors(node))
        if not children:
            return {"id": node, **G.nodes[node]}
        return {
            "id": node,
            **G.nodes[node],
            "subareas": [recurse(child) for child in children],
        }

    return recurse(root_id)


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
    Main function to read map data, construct a graph, and output a nested JSON structure.

    主函数用于读取地图数据，构建图结构，并输出嵌套的 JSON 结构。
    """
    map = Waifu()
    map.read(mode="file", file_path="map.osm")  # Assuming this reads map data
    G = build_graph(map)

    strategy = "auto"  # Can be "auto", "input", "highest"
    try:
        root_id = find_root_node_id(
            G, strategy
        )  # Find the root node ID based on strategy
        nested_json = graph_to_nested_json(G, root_id)
        json_output = json.dumps(nested_json, indent=2, ensure_ascii=False)
        print(json_output)
        with open("map.json", "w", encoding="utf-8") as f:
            f.write(json_output)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
