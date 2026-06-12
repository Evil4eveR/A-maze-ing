from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from typing import ClassVar

import sys


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=sys.argv[1] if len(sys.argv) > 1 else None,
        env_file_encoding="utf-8",
    )

    wall: ClassVar[str] = "\u2588\u2588"
    cell: ClassVar[str] = "  "
    cell = wall
    path: ClassVar[str] = "\u2591\u2591"
    width: int
    height: int
    entry_raw: str = Field(alias="entry")
    exit_raw: str = Field(alias="exit")
    output_file: str
    perfect: bool
    seed: int | None = None
    themes_path: str = "themes.json"

    @computed_field
    @property
    def entry(self) -> tuple[int, int]:
        x, y = self.entry_raw.split(',')
        return int(x), int(y)

    @computed_field
    @property
    def exit(self) -> tuple[int, int]:
        x, y = self.exit_raw.split(',')
        return int(x), int(y)


settings = Settings()
