import importlib.util
import os
import sys
from typing import Optional

import typer

from advent_of_py import __app_name__, __version__, utils

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


@app.command(name="new", help="Create a new day for the current year.")
def new() -> None:
    year, aoc_session = utils.get_variables("YEAR", "AOC_SESSION")
    year_dir = year
    if not os.path.exists(year_dir):
        os.mkdir(year_dir)
    last_day = utils.get_last_day(year)
    next_day = last_day + 1
    next_day_str = f"{next_day:02d}"
    if not os.path.exists(os.path.join(year_dir, f"day{next_day_str}")):
        os.mkdir(os.path.join(year_dir, f"day{next_day_str}"))

    new_file_path = os.path.join(year_dir, f"day{next_day_str}/day.py")

    with open(new_file_path, "w") as new_file:
        new_file.write(f"# Advent of Code {year} - Day {next_day}\n\n")
        new_file.write(utils.get_template(year, next_day_str))

    utils.get_input(year, int(next_day))
    utils.get_instructions(year, int(next_day))
    return


@app.command(name="update", help="Update the instructions for the last day.")
def update() -> None:
    year, _ = utils.get_variables("YEAR", "AOC_SESSION")
    day = utils.get_last_day(year)
    utils.get_instructions(year, day)
    return


@app.command(name="run", help="Run the last day solution.")
def run() -> None:
    year = utils.get_variables("YEAR")[0]
    day = utils.get_last_day(int(year))
    if day == 0:
        print(f"No days available for year {year}")
        sys.exit(1)
    day_str = f"{day:02d}"
    module_path = f"{year}/day{day_str}/day.py"
    module_name = module_path.replace("/", ".").replace(".py", "")
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return
