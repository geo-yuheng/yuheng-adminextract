LOCALE = "zh"


def i18n_string(strid: str) -> str:
    """Returns a localized string based on the given string ID.

    This function looks up a localized version of a text string using its unique string identifier. It's useful for internationalization (i18n) in applications that support multiple languages.

    Args:
        strid: A string identifier for the desired text.

    Returns:
        A localized string corresponding to the given ID.

    根据给定的字符串 ID 返回本地化字符串。

    该函数使用其唯一字符串标识符查找文本字符串的本地化版本。它适用于支持多种语言的应用程序中的国际化（i18n）。

    参数:
        strid: 所需文本的字符串标识符。

    返回:
        与给定 ID 对应的本地化字符串。
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
            "export_plain_json_help": "JSON schema format: nest or plain.",
            "root_select_strategy_help": "Strategy to select the root node. Default is 'auto'.",
            "description": "Process map data and output JSON.",
            "error_conflict": "Error: STOP_LEVEL and ONLY_LEVEL cannot both be set.",
            "json_output": "JSON output has been written to {output_file}.",
            "wrong-vis-method": "Invalid visualization method. Choose 'plt' or 'gv'.",
            "output_format_help": "Output format: json or gv.",
            "ensure_connected_help": "Ensure all nodes are connected to the root node.",
            "error_exception": "An error occurred: {error_message}",
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
            "export_plain_json_help": "JSON模式格式：嵌套或平铺。",
            "root_select_strategy_help": "选择根节点的策略。默认为'auto'。",
            "description": "处理地图数据并输出JSON。",
            "error_conflict": "错误：STOP_LEVEL和ONLY_LEVEL不能同时设置。",
            "json_output": "JSON输出已写入{output_file}。",
            "wrong-vis-method": "无效的可视化方法。请选择'plt'或'gv'。",
            "output_format_help": "指定输出格式：json 或 gv。",
            "ensure_connected_help": "确保所有节点都与根节点相连。",
            "error_exception": "发生错误：{error_message}",
        },
    }
    return strings.get(LOCALE, {}).get(strid, "")
