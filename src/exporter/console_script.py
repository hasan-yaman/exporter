import sys
import argparse
from .exporter import export
from .image_exporter import image_export, get_all_styles
from .exceptions import UnsupportedFileError

# Prepare command line interface
export_parser = argparse.ArgumentParser(description='Export Jupyter Notebooks as Python scripts.')
export_parser.add_argument('notebook_path', type=str, help="Path of the Jupyter notebook.")
export_parser.add_argument('output_path', type=str, help="Path of the output script.")
export_parser.add_argument('--delete_export_comments', '-dc', action='store_true',
                           help="If exists, then #export comments will be deleted from output script.")
#  TODO: Add default value
export_parser.add_argument('--cell-seperator', '-cs',
                           help='String that seperates exported cells.Default to 2 newlines.')

image_export_parser = argparse.ArgumentParser(description="")
image_export_parser.add_argument('input_path', type=str, help="Path of the input file.")
image_export_parser.add_argument('output_base_path', type=str, help="Base path for the output images.")
image_export_parser.add_argument('style', type=str, help="Style of the output images.")
# TODO: list of styles
image_export_parser.add_argument('')


def run_export_console_script():
    """
    Run export() function from command line.
    """

    #  Parse command line arguments
    args = export_parser.parse_args(args=sys.argv[1:])
    try:
        export(args.notebook_path, args.output_path, args.delete_export_comments, args.cell_seperator)
    except FileNotFoundError as e:
        print(f"Notebook file not found. {e} not exists.")


def run_image_export_console_script():
    """
    Run image_export() or get_all_styles() functions from command line.
    """
    args = image_export_parser.parse_args(args=sys.argv[1:])
    try:
        #todo if-else
        image_export(args.input_path, args.output_base_path, args.style)
    except FileNotFoundError as e:
        print(f"File not found. {e} not exists.")
    except UnsupportedFileError as e:
        print(f"Extension of {e} is not supported. Support extensions are: .py and .ipynb")
