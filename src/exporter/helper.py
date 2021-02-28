import nbformat
from pathlib import Path
from typing import List


def read_notebook(notebook_path: Path) -> List:
    """
    Read Jupyter Notebook

    Parameters
    ----------
    notebook_path: Path
                Path of the Jupyter notebook.
    Returns
    ------
    cells: List
                List of code blocks.
    """
    with open(notebook_path, 'r', encoding='utf-8') as inp:
        notebook = nbformat.reads(inp.read(), as_version=4)
    blocks = []
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            blocks.append(cell['source'])
    return blocks


def read_script(script_path: Path) -> List:
    """
    Read Python script

    Parameters
    ----------
    script_path: Path
                Path of the Pythons scripts.
    Returns
    ------
    lines: List
                List of code lines.
    """
    with open(script_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines


def is_notebook(path: Path) -> bool:
    """
    Checks whether the given file path is Jupyter Notebook or not.

    Parameters
    ----------
    path: Path
        Path of the file to check whether it is Jupyter Notebook or not.
    Returns
    ------
    Returns True when file is Jupyter Notebook, False otherwise.
    """
    if path.suffix == ".ipynb":
        return True
    return False


def is_script(path: Path) -> bool:
    """
    Checks whether the given file path is Python script or not.

    Parameters
    ----------
    path: Path
        Path of the file to check whether it is Python script or not.
    Returns
    ------
    Returns True when file is Python script, False otherwise.
    """
    if path.suffix == ".py":
        return True
    return False
