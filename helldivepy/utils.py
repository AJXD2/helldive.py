import re
from helldivepy.constants import FACTIONS
import helldivepy.enums as enums


def hdml_to_md(text: str) -> str:
    """
    Converts a string in HDML (DiveHarder Markup Language) format to Markdown format.

    Args:
        text (str): The input string in HDML format.

    Returns:
        str: The input string converted to Markdown format.

    Example:
        >>> hdml_to_md("<i=3>Hello</i=3> <i=1>World</i=1>")
        "[b]Hello[/b] [yellow]World[/yellow]"
    """

    pattern = r"<i=(\d+)>(.*?)<\/i(?:=\1)?>"
    matches = re.findall(pattern, text)

    modified_text = text
    for match in matches:
        if match[0] == "3":
            modified_text = modified_text.replace(match[1], f"[b]{match[1]}[/b]")
        elif match[0] == "1":
            modified_text = modified_text.replace(
                match[1], f"[yellow]{match[1]}[/yellow]"
            )

    modified_text = re.sub(r"<\/?i(?:=\d+)?>", "", modified_text)

    return modified_text


def url_join(*args):
    """Join combine URL parts to get the full endpoint address."""
    return "/".join(arg.strip("/") for arg in args)


def parse_faction(faction: int) -> enums.FactionType | None:
    """Parse faction ID to string

    Args:
        faction (int): The faction ID

    Returns:
        str: The faction name
    """
    return FACTIONS.get(faction, None)  # type: ignore


class DiveHarderException(Exception):
    """Base exception for all DiveHarder exceptions."""


class DiveHarderAPIConnectionError(DiveHarderException):
    """Exception raised when the DiveHarder API connection fails."""
