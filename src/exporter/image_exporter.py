import re
import io
from typing import List
from pathlib import Path
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles
import codecs
import imgkit
from .monkey_patch import patched_open
from .exceptions import StyleNotFoundError
from .helper import read_script, read_notebook, is_notebook, is_script
from .exceptions import UnsupportedFileError

#  Monkey patch
codecs.open = patched_open

_image_export_block_start_pattern = r"^#\s*image-export-start\s*$"
_image_export_block_end_pattern = r"^#\s*image-export-end\s*$"
_flags = re.IGNORECASE | re.MULTILINE


def _parse_blocks(input_path: Path) -> List:
    """
    Read a file and returns list that each member contains code blocks that will be exported as image.

    Parameters
    ----------
    input_path: Path
        Path of the input file.
    Returns
    ------
    exported_blocks: List
        Return list that each member contains code block that is between image export comments.
    """
    if is_notebook(input_path):
        lines = read_notebook(input_path)
    elif is_script(input_path):
        lines = read_script(input_path)
    else:
        raise UnsupportedFileError(input_path)

    exported_blocks = []
    block_started = False
    for line in lines:
        #  Search start of the block
        if not block_started and re.search(_image_export_block_start_pattern, line,
                                           _flags) is not None:
            #  Start of the block
            block_started = True
            exported_blocks.append("")
            continue
        if block_started and re.search(_image_export_block_end_pattern, line, _flags) is not None:
            #  End of the block
            block_started = False
            continue
        if block_started:
            exported_blocks[-1] = exported_blocks[-1] + line.replace(u'\xa0', u' ')
    return exported_blocks


def available_styles() -> List:
    """
    Returns all the available styles.

    Returns:
        Returns list of all the available styles.
    """
    return list(get_all_styles())


def image_export(input_path: str, output_base_path: str, style: str):
    """
    Export code (Python script or Jupyter Notebook) as a image.

        Parameters
    ----------
    input_path: str
                    Path of the file that contains cells to be exported.
    output_base_path: str
                    Base path of the exported images. If two images are exported, then paths for them will
                    be 'output_base_path_0.jpg' and 'output_base_path_1.jpg'
    style: bool
                    Style of the exported image. For the list of supported styles use 'available_styles()'
                    function.
    Returns
    ------
    None
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(input_path)
    #  Check code_format is valid
    if style not in available_styles():
        raise StyleNotFoundError(style)
    blocks = _parse_blocks(input_path)
    lexer = PythonLexer()
    formatter = HtmlFormatter(style=style)

    for i, block in enumerate(blocks):
        highlighted_block = highlight(block, lexer, formatter)
        #  We are closing StringIO after reading it, therefore we need to recreate it.
        css_buffer = io.StringIO(formatter.get_style_defs('.highlight'))
        imgkit.from_string(highlighted_block, f"{output_base_path}-{i}.jpg", css=css_buffer)
