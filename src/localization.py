LOCALE = "zh"


prompt.find_root_node_id.root_node_id ==> prompt.find_root_node_id.root_node_id
error.find_root_node_id.no_root_node_found ==> error.find_root_node_id.no_root_node_found
prompt.find_root_node_id.manual_root_node_id ==> prompt.find_root_node_id.manual_root_node_id
error.find_root_node_id.error_invalid_node_id ==> error.find_root_node_id.error_invalid_node_id
error.find_root_node_id.error_invalid_number ==> error.find_root_node_id.error_invalid_number
prompt.find_root_node_id.multiple_root_nodes ==> prompt.find_root_node_id.multiple_root_nodes
help.main.input_file ==> help.main.input_file
help.main.output_file ==> help.main.output_file
help.main.stop_level ==> help.main.stop_level
help.main.only_level ==> help.main.only_level
help.main.json_schema ==> help.main.json_schema
help.main.root_select_strategy ==> help.main.root_select_strategy
description.main.app_function ==> description.main.app_function
error.main.conflict_stop_level_and_only_level ==> error.main.conflict_stop_level_and_only_level
message.main.json_output_written ==> message.main.json_output_written
error.visualize_graph.invalid_method ==> error.visualize_graph.invalid_method
help.main.output_format ==> help.main.output_format
help.main.ensure_connected ==> help.main.ensure_connected
error.main.general_error ==> error.main.general_error

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
            "prompt.find_root_node_id.root_node_id": "Please enter the root node ID:",
            "error.find_root_node_id.no_root_node_found": "Unable to find root node ID, please ensure the graph contains administrative boundary nodes.",
            "prompt.find_root_node_id.manual_root_node_id": "Unable to automatically determine the root node ID, please enter manually:",
            "error.find_root_node_id.error_invalid_node_id": "The entered ID is invalid, please enter a valid node ID.",
            "error.find_root_node_id.error_invalid_number": "Please enter a valid number.",
            "prompt.find_root_node_id.multiple_root_nodes": "Multiple root nodes of the same highest level found, please choose one as the root node:",
            "help.main.input_file": "Path to the input map file.",
            "help.main.output_file": "Path to the output JSON file.",
            "help.main.stop_level": "Set the desired stop level. Cannot be used with --only-level.",
            "help.main.only_level": "Set the level to exclusively include. Cannot be used with --stop-level.",
            "help.main.json_schema": "JSON schema format: nest or plain.",
            "help.main.root_select_strategy": "Strategy to select the root node. Default is 'auto'.",
            "description.main.app_function": "Process map data and output JSON.",
            "error.main.conflict_stop_level_and_only_level": "Error: STOP_LEVEL and ONLY_LEVEL cannot both be set.",
            "message.main.json_output_written": "JSON output has been written to {output_file}.",
            "error.visualize_graph.invalid_method": "Invalid visualization method. Choose 'plt' or 'gv'.",
            "help.main.output_format": "Output format: json or gv.",
            "help.main.ensure_connected": "Ensure all nodes are connected to the root node.",
            "error.main.general_error": "An error occurred: {error_message}",
        },
        "zh": {
            "prompt.find_root_node_id.root_node_id": "请输入根节点ID：",
            "error.find_root_node_id.no_root_node_found": "无法找到根节点ID，请确保图中包含行政边界节点。",
            "prompt.find_root_node_id.manual_root_node_id": "无法自动确定根节点ID，请手动输入：",
            "error.find_root_node_id.error_invalid_node_id": "输入的ID无效，请输入有效的节点ID。",
            "error.find_root_node_id.error_invalid_number": "请输入一个有效的数字。",
            "prompt.find_root_node_id.multiple_root_nodes": "发现多个同等最高级别的节点，请选择一个作为根节点：",
            "help.main.input_file": "输入地图文件的路径。",
            "help.main.output_file": "输出JSON文件的路径。",
            "help.main.stop_level": "设置所需的终止级别。不能与--only-level一起使用。",
            "help.main.only_level": "设置仅包含的级别。不能与--stop-level一起使用。",
            "help.main.json_schema": "JSON模式格式：嵌套或平铺。",
            "help.main.root_select_strategy": "选择根节点的策略。默认为'auto'。",
            "description.main.app_function": "处理地图数据并输出JSON。",
            "error.main.conflict_stop_level_and_only_level": "错误：STOP_LEVEL和ONLY_LEVEL不能同时设置。",
            "message.main.json_output_written": "JSON输出已写入{output_file}。",
            "error.visualize_graph.invalid_method": "无效的可视化方法。请选择'plt'或'gv'。",
            "help.main.output_format": "指定输出格式：json 或 gv。",
            "help.main.ensure_connected": "确保所有节点都与根节点相连。",
            "error.main.general_error": "发生错误：{error_message}",
        },
    }
    return strings.get(LOCALE, {}).get(strid, "")
