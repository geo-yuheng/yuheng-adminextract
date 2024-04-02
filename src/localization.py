import json
from typing import Any, Dict

JSON_FILE_PATH = "localization.json"
LOCALE = "zh"


def load_localization_strings() -> Dict[str, Any]:
    """Loads localization strings from a JSON file.

    This function reads a JSON file from the disk and parses it into a dictionary. It's used for loading localized strings for internationalization purposes.

    Raises:
        Exception: If the JSON file is not found or is not a valid JSON.

    Returns:
        A dictionary containing the localized strings.
    
    从JSON文件加载本地化字符串。

    此函数从磁盘读取一个JSON文件，并将其解析为字典。用于加载本地化字符串，以支持国际化。

    抛出异常：
        如果JSON文件未找到或不是有效的JSON，则抛出异常。

    返回：
        包含本地化字符串的字典。
    """
    try:
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise Exception(f"Localization file {JSON_FILE_PATH} not found.")
    except json.JSONDecodeError:
        raise Exception(
            f"Localization file {JSON_FILE_PATH} is not a valid JSON."
        )


def i18n_string(strid: str) -> str:
    """Returns a localized string based on the given string ID.

    This function looks up a localized version of a text string using its unique string identifier. It's useful for internationalization (i18n) in applications that support multiple languages. If the string ID is not found, it returns a default message in the current locale.

    Args:
        strid: A string identifier for the desired text.

    Returns:
        A localized string corresponding to the given ID or a default message if the ID is not found.
    
    根据给定的字符串ID返回本地化字符串。

    此函数使用其唯一字符串标识符查找文本字符串的本地化版本。对于支持多种语言的应用程序中的国际化（i18n）非常有用。如果未找到字符串ID，则返回当前语言环境的默认消息。

    参数：
        strid: 想要的文本的字符串标识符。

    返回：
        对应于给定ID的本地化字符串，如果未找到ID，则返回默认消息。
    """
    strings = load_localization_strings()

    localized_strings = strings.get(LOCALE, {})
    localized_string = localized_strings.get(strid)

    if localized_string is None:
        default_messages = {
            "en": f"String ID '{strid}' not found.",
            "zh": f"未找到字符串ID '{strid}'。",
        }
        return default_messages.get(LOCALE, f"String ID '{strid}' not found.")

    return localized_string
