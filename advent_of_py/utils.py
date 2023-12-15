import os
import re
import sys
from typing import Tuple

import markdownify
import requests
from bs4 import BeautifulSoup


def get_variables(*args) -> Tuple:
    errors = []
    variables = []
    for arg in args:
        var = os.environ.get(arg)
        if var is None:
            errors.append(f"{arg} environment variable not set")
        variables.append(var)
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    return tuple(variables)


def get_last_day(year: int) -> int:
    days = []
    for root, dirs, files in os.walk(str(year)):
        for directory in dirs:
            match = re.match(r"day(\d+)", directory)
            if match:
                days.append(int(match.group(1)))
    if len(days) == 0:
        return 0
    return int(days[-1])


def get_instructions(year: int, day: int) -> None:
    day_str = f"{day:02d}"
    url = f"https://adventofcode.com/{year}/day/{day}"
    cookies = {"session": os.getenv("AOC_SESSION")}
    resp = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(resp.content, "html.parser")

    instructions = soup.find_all("article", attrs={"class": "day-desc"})
    instructions = "\n".join([str(desc) for desc in instructions]) + "\n"

    h = (
        markdownify.markdownify(str(instructions), heading_style="ATX").rstrip("\n")
        + "\n"
    )
    f = open(f"{year}/day{day_str}/instructions.md", "w")
    f.write(h)
    f.close()


def get_input(year: int, day: int) -> None:
    day_str = f"{day:02d}"
    url = f"https://adventofcode.com/{year}/day/{day_str}/input"
    cookies = {"session": os.getenv("AOC_SESSION")}
    resp = requests.get(url, cookies=cookies)
    input_data = resp.text

    open(f"{year}/day{day_str}/example.txt", "w")
    f = open(f"{year}/day{day_str}/data.txt", "w")
    f.write(input_data)
    f.close()


def get_template(year: int, day: str) -> str:
    template = """from advent_of_py import AdventDay


class Day(AdventDay):
    test_files = {"{YEAR}/day{DAY}/example.txt": [None, None]}
    data_file = "{YEAR}/day{DAY}/data.txt"

    def parse_file(self, data):
        return data.split("\\n")[:-1]

    def part_1_logic(self, data):
        return None

    def part_2_logic(self, data):
        return None

Day()
""".replace(
        "{YEAR}", str(year)
    ).replace(
        "{DAY}", day
    )
    return template
