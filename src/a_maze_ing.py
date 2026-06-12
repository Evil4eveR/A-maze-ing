from random import randint

from rich.live import Live
from dispatcher import Dispatcher

from mazegen.hooks.break_perfect import BreakPerfect
from models.theme import Theme

from mazegen.models.maze import Maze
from config import settings

from utils.file import save_maze_to_file
from utils.maze_config import make_maze_config

from utils.ui import build_ui, ThemeGenerator
from mazegen.maze_solver import MazeSolver

from mazegen.maze_generator import MazeGenerator
from renderer.ascii import AsciiMazeRenderer


dp = Dispatcher()
maze_config = make_maze_config()


def render_maze(live: Live, maze: Maze, theme: Theme) -> AsciiMazeRenderer:
    path = dp.data.get('path') if dp.data.get('is_path_shown') else None
    renderer = AsciiMazeRenderer(maze, themes=theme, path=path)
    live.update(build_ui(
        renderer.render(),
        dp.get_help(),
        maze.algo or '',
        theme.name,
        maze_config.seed
    ))
    return renderer


def refresh_path(maze: Maze) -> None:
    if dp.data.get('path'):
        dp.data['path'] = MazeSolver.solve(maze)
        dp.data['is_new_maze'] = False


def save_file() -> None:
    maze = dp.data['maze']
    path = dp.data.get('path')
    if not path:
        path = MazeSolver.solve(maze)
        dp.data['path'] = path
        dp.data['is_new_maze'] = False
    if path is None:
        return
    save_maze_to_file(maze, path, settings.output_file)


@dp.startup
def startup(live: Live) -> None:
    if maze_config.seed is None:
        maze_config.seed = randint(1, 100000000000000)
    maze = MazeGenerator.create(config=maze_config)
    theme = next(dp.data['theme_gen'])
    dp.data['maze'] = maze
    dp.data['theme'] = theme
    dp.data['is_new_maze'] = True
    render_maze(live, maze, theme)
    save_file()


@dp.shutdown
def shutdown() -> None:
    print("Bye!")


@dp.on('r', help="Regenerate the maze")
def regenerate_maze(live: Live, theme: Theme) -> None:
    maze_config.seed = randint(1, 100000000000000)
    maze = MazeGenerator.create(config=maze_config)
    dp.data['is_new_maze'] = True
    dp.data['maze'] = maze
    refresh_path(maze)
    render_maze(live, maze, theme)
    save_file()


@dp.on('n', help="Next theme")
def swap_colors(live: Live, maze: Maze, theme_gen: ThemeGenerator) -> None:
    theme = next(theme_gen)
    dp.data['theme'] = theme
    render_maze(live, maze, theme)


@dp.on('b', help="Previous theme")
def previous_theme(live: Live, maze: Maze, theme_gen: ThemeGenerator) -> None:
    theme = theme_gen.prev()
    dp.data['theme'] = theme
    render_maze(live, maze, theme)


@dp.on('p', help="Show/hide the solution path")
def solve_maze(live: Live, maze: Maze, theme: Theme) -> None:
    if dp.data.get('is_path_shown'):
        dp.data['is_path_shown'] = False
    else:
        dp.data['is_path_shown'] = True
        if dp.data.get('is_new_maze'):
            dp.data['path'] = MazeSolver.solve(maze)
            dp.data['is_new_maze'] = False

    render_maze(live, maze, theme)


@dp.on('a', help="Animate the maze generation and solving")
def animate_maze_path(live: Live, theme: Theme) -> None:
    dp.data['is_path_shown'] = False
    for maze in MazeGenerator.create_animated(config=maze_config):
        renderer = render_maze(live, maze, theme)

    for path, is_final in MazeSolver.solve_animated(maze):
        renderer.connect = is_final
        renderer.path = path
        live.update(build_ui(
            renderer.render(),
            dp.get_help(),
            maze.algo or '',
            theme.name,
            maze_config.seed
        ))
    dp.data['path'] = path
    dp.data['is_path_shown'] = True
    dp.data['is_new_maze'] = False


@dp.on("m", help="Animate the maze generation")
def animate_maze(live: Live, theme: Theme) -> None:
    is_path = dp.data.get('is_path_shown')
    dp.data['is_path_shown'] = False
    for maze in MazeGenerator.create_animated(config=maze_config):
        render_maze(live, maze, theme)
    if is_path:
        dp.data['is_path_shown'] = True
        render_maze(live, maze, theme)


@dp.on("t", help="Animate the maze solving")
def animate_path(live: Live, maze: Maze, theme: Theme) -> None:
    renderer = AsciiMazeRenderer(maze, themes=theme)
    for path, is_final in MazeSolver.solve_animated(maze):
        renderer.connect = is_final
        renderer.path = path
        live.update(build_ui(
            renderer.render(),
            dp.get_help(),
            maze.algo or '',
            theme.name,
            maze_config.seed
        ))
    dp.data['path'] = path
    dp.data['is_path_shown'] = True
    dp.data['is_new_maze'] = False


@dp.on('w', help="Swap algorithms")
def swap_algorithm(live: Live, maze: Maze, theme: Theme) -> None:
    algos = list(MazeGenerator.ALGO_MAP.keys())
    current_algo = maze_config.algo
    assert isinstance(current_algo, str)
    next_algo = algos[(algos.index(current_algo) + 1) % len(algos)]
    maze_config.algo = next_algo
    maze = MazeGenerator.create(config=maze_config)
    dp.data['maze'] = maze
    refresh_path(maze)
    render_maze(live, maze, theme)
    save_file()


@dp.on('v', help="Switch perfect/imperfect maze")
def switch_perfect_imperfect(live: Live, maze: Maze, theme: Theme) -> None:
    if maze_config.hooks is None:
        maze_config.hooks = []
    for hook in maze_config.hooks:
        if isinstance(hook, BreakPerfect):
            maze_config.hooks.remove(hook)
            break
    else:
        maze_config.hooks.append(
            BreakPerfect(percent=0.1, seed=maze_config.seed)
        )
    maze = MazeGenerator.create(config=maze_config)
    dp.data['maze'] = maze
    refresh_path(maze)
    render_maze(live, maze, theme)
    save_file()


@dp.on('q', help="Quit the application")
def quit_app() -> None:
    dp.stop()


if __name__ == "__main__":
    dp.data['theme_gen'] = ThemeGenerator(settings.themes_path)
    dp.run(30)
