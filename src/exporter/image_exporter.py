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
from .exceptions import UnsupportedFileExtensionError
from .constants import _supported_image_formats, _supported_file_formats

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
        raise UnsupportedFileExtensionError(input_path, _supported_file_formats)

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


def image_export(input_path: str, output_path: str, style: str, zoom: float = 2.0):
    """
    Export code (Python script or Jupyter Notebook) as a image.

        Parameters
    ----------
    input_path: str
                    Path of the file that contains cells to be exported.
    output_path: str
                    Output path of the exported images. If two images are exported, then paths for them will
                    be '0_output_path' and '1_output_path'
    style: bool
                    Style of the exported image. For the list of supported styles use 'available_styles()'
                    function.
    zoom: float
                    Zoom factor for the output image.
    Returns
    ------
    None
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    if not input_path.exists():
        raise FileNotFoundError(input_path)
    #  Check style is valid
    if style not in available_styles():
        raise StyleNotFoundError(style)
    if output_path.suffix not in _supported_image_formats:
        raise UnsupportedFileExtensionError(output_path, _supported_image_formats)
    blocks = _parse_blocks(input_path)
    lexer = PythonLexer()
    formatter = HtmlFormatter(style=style)

    #  Options for imgkit
    options = {
        'quiet': '',  #  Do not show any output
        'zoom': zoom,  #  Zoom level
    }

    for i, block in enumerate(blocks):
        highlighted_block = highlight(block, lexer, formatter)
        #  We are closing StringIO after reading it, therefore we need to recreate it.
        css_buffer = io.StringIO(formatter.get_style_defs('.highlight'))
        output_path_formatted = f"{output_path}" if len(blocks) == 1 else f"{i}_{output_path}"
        imgkit.from_string(highlighted_block, output_path_formatted, css=css_buffer, options=options)
