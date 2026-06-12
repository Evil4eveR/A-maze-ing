from rich.live import Live
from typing import Any, Callable, Dict

import queue
import threading

import inspect
import readchar


class Dispatcher:
    def __init__(self):
        self._handlers: dict[str, Callable[..., Any]] = {}
        self.data: Dict[str, Any] = {}
        self.command_help: Dict[str, str] = {}
        self._startup: Callable[[Live], None] | None = None
        self._shutdown: Callable[[], None] | None = None
        self._running = True

    def get_help(self) -> str:
        lines: list[str] = []
        for i, (key, text) in enumerate(self.command_help.items()):
            lines.append(
                f"{i+1}. [bold cyan]{key}[/bold cyan]: {text}"
            )
        return "\n".join(lines)

    def startup(self, func: Callable[[Live], None]) -> Callable[[Live], None]:
        self._startup = func
        return func

    def shutdown(self, func: Callable[[], None]) -> Callable[[], None]:
        self._shutdown = func
        return func

    def on(
        self, key: str, help: str = ""
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self._handlers[key] = func
            self.command_help[key] = help
            return func
        return decorator

    def dispatch(self, key: str, **kwargs: dict[str, Any]) -> bool:
        if key in self._handlers:
            func = self._handlers[key]
            kw = self._filter_params(func, **kwargs)
            func(**kw)
            return True
        return False

    def _filter_params(
        self,
        func: Callable[..., Any],
        **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        kw: dict[str, Any] = {}
        params = inspect.signature(func).parameters
        data = self.data.copy()
        data.update(kwargs)

        for name, param in params.items():
            annotation = param.annotation
            if annotation is inspect.Parameter.empty:
                continue
            for value in data.values():
                try:
                    if isinstance(value, annotation):
                        kw[name] = value
                        break
                except TypeError:
                    continue
        return kw

    def run(self, refresh_per_second: int = 10) -> None:
        self._running = True
        _busy = False
        key_queue: queue.Queue[str] = queue.Queue()

        def read_keys() -> None:
            while self._running:
                key = readchar.readkey()
                if not _busy:
                    key_queue.put(key)

        reader = threading.Thread(target=read_keys, daemon=True)
        reader.start()

        with Live(refresh_per_second=refresh_per_second, screen=True) as live:
            self.data['live'] = live

            if self._startup:
                self._startup(live)

            while self._running:
                try:
                    key = key_queue.get()
                except queue.Empty:
                    continue

                _busy = True
                try:
                    self.dispatch(key)
                finally:
                    _busy = False

        if self._shutdown:
            self._shutdown()

    def stop(self) -> None:
        self._running = False
