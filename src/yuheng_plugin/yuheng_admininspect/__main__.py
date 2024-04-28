import argparse

from __init__ import main

if __name__ == "__main__":
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
    main()
