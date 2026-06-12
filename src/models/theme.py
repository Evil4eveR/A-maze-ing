from dataclasses import dataclass


@dataclass
class Theme:
    """Colour theme for maze rendering."""
    name: str = "Default"
    cell: str = "#000000"
    wall: str = "#2596BE"
    blocked_cell: str = "#757575"
    path: str = "#FFFF00"
    entry: str = "#FF00FF"
    exit: str = "#FF0000"
