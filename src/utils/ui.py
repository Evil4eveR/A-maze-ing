from models.theme import Theme
import json


def build_ui(
    render_str: str,
    helper_str: str,
    algo: str,
    theme_name: str,
    maze_seed: int | None = None
) -> str:
    text = (
        f"{render_str}\n\n"
        f"A-maze-ing - A Maze Generator and Solver\n"
        f"Press buttons to interact with the maze:\n"
        f"Theme: {theme_name}\n"
        f"Algorithm: {algo}\n"
        f"Maze Seed: {maze_seed or 'N/A'}\n"
        f"{helper_str}\n"
    )
    return text


class ThemeGenerator:
    def __init__(self, themes_file: str = 'themes.json') -> None:
        with open(themes_file, 'r') as f:
            self.themes_data = json.load(f)
        self.index = -1

    def __iter__(self) -> "ThemeGenerator":
        return self

    def __next__(self) -> Theme:
        if not self.themes_data:
            raise StopIteration
        self.index = (self.index + 1) % len(self.themes_data)
        theme = self.themes_data[self.index]
        return Theme(**theme)

    def prev(self) -> Theme:
        if not self.themes_data:
            raise StopIteration
        self.index = (self.index - 1) % len(self.themes_data)
        theme = self.themes_data[self.index]
        return Theme(**theme)
