import os
import time
from copy import deepcopy
from typing import Any, Dict, List


def color(text, cl):
    colors = {"green": "\033[92m", "red": "\033[91m"}
    return colors[cl] + text + "\033[0m"


def log(text, depth=0):
    print("  " * depth + text)


class AdventDay:
    test_files: Dict[str, List] = {}
    data_file: str = ""

    def __init__(self):
        self.test_data = [self.read_file(test_file) for test_file in self.test_files]
        self.test_data = []
        self.test_solutions = []
        for test_file, test_solution in self.test_files.items():
            self.test_data.append(self.read_file(test_file))
            self.test_solutions.append(test_solution)
        self.data = self.read_file(self.data_file)
        self._funcs = [self.part_1_logic, self.part_2_logic]
        self.run()

    def read_file(self, file: str) -> str:
        if not os.path.exists(file):
            raise FileNotFoundError(f"Input data file ({file}) missing")
        file_data = open(file, "r").read()
        return self.parse_file(file_data)

    def parse_file(self, file_data: str) -> Any:
        return file_data.split(",")

    def part_1_logic(self, data: Any) -> Any:
        return None

    def part_2_logic(self, data: Any) -> Any:
        return None

    def _run_part_test(self, index) -> bool:
        for i, test_data in enumerate(self.test_data):
            test_data = deepcopy(test_data)
            expected = self.test_solutions[i][index]
            result = self._funcs[index](test_data)
            if not result == expected:
                log(
                    f" {color('x', 'red')} Test {i + 1}: {result} (expected {expected})"
                )
                return False
            else:
                log(f"{color('✓', 'green')} Test {i + 1}: {result}")
        return True

    def _run_part(self, index) -> Any:
        log(f"----- Running part {index + 1} -----")
        if self._run_part_test(index):
            data = deepcopy(self.data)
            start = time.perf_counter()
            result = self._funcs[index](data)
            end = time.perf_counter()
            exec_time = round((end - start) * 1000, 2)
            if exec_time > 1000:
                exec_time = str(exec_time / 1000) + "s"
            else:
                exec_time = str(exec_time) + "ms"
            log(f"Result: {result} ({exec_time})", 1)
            return True
        return False

    def run(self) -> Any:
        if self._run_part(0):
            self._run_part(1)
