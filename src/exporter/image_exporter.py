import re
import io
from pathlib import Path
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles
import codecs
import imgkit
from src.exporter.monkey_patch import patched_open
from src.exporter.exceptions import StyleNotFoundError

#  Monkey patch
codecs.open = patched_open
_image_export_block_start_pattern = r"^#\s*image-export-start\s*$"
_image_export_block_end_pattern = r"^#\s*image-export-end\s*$"
_flags = re.IGNORECASE | re.MULTILINE


def _read_script(script_path: str):
    with open(script_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
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
    print(exported_blocks)
    return exported_blocks


def image_export(input_path: str, output_base_path: str, style: str):
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(input_path)
    #  Check code_format is valid
    if style not in list(get_all_styles()):
        raise StyleNotFoundError(style)
    if input_path.suffix == ".py":
        blocks = _read_script(input_path)
    else:
        blocks = []
    #  TODO: Refactor reading
    lexer = PythonLexer()
    formatter = HtmlFormatter(style=style)

    for i, block in enumerate(blocks):
        highlighted_block = highlight(block, lexer, formatter)
        #  We are closing StringIO after reading it, therefore we need to recreate it.
        css_buffer = io.StringIO(formatter.get_style_defs('.highlight'))
        imgkit.from_string(highlighted_block, f"{output_base_path}-{i}.jpg", css=css_buffer)


