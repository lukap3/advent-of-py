from setuptools import find_packages, setup

setup(
    name="advent-of-py",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "typer~=0.9.0",
        "setuptools~=68.2.2",
        "markdownify~=0.11.6",
        "requests~=2.31.0",
        "bs4~=0.0.1",
        "beautifulsoup4~=4.12.2",
    ],
    entry_points={
        "console_scripts": [
            "advent-of-py=advent_of_py.__main__:main",
        ],
    },
)
