import nbformat
import re
from pathlib import Path

_pattern = r"^#\s*export\s*$"
_flags = re.IGNORECASE | re.MULTILINE


def export(notebook_path: str, output_path: str, delete_export_comments: bool = False):
    """
    TODO: Add docstring.
    """

    notebook_path = Path(notebook_path)
    output_path = Path(output_path)
    if not notebook_path.exists():
        raise FileNotFoundError(notebook_path)
    # Read notebook
    with open(notebook_path, 'r', encoding='utf-8') as inp:
        notebook = nbformat.reads(inp.read(), as_version=4)
    # Iterate over cells
    sources = []
    for cell in notebook['cells']:
        #  Find cells that will be exported
        if cell['cell_type'] == 'code' and re.search(_pattern, cell['source'], _flags) is not None:
            if delete_export_comments:
                source = re.sub(_pattern, '', cell['source'], flags=_flags)
            else:
                source = cell['source']
            sources.append(source)
    if len(sources) > 0:
        #  Write source codes to output file
        with open(output_path, 'w', encoding='UTF-8') as out:
            out.write(f"# THIS SCRIPT IS AUTOGENERATED FROM {notebook_path}. \n\n")
            for index, source in enumerate(sources):
                if not delete_export_comments:
                    out.write("\n")
                out.write(source)
                if index == len(sources) - 1:
                    # Put single new line at the end of script.
                    out.write("\n")
                else:
                    # Put double new line between different cells.
                    out.write("\n\n")

    else:
        print("No cell exported.")
