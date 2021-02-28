import sys
import argparse
from .exporter import export

# Prepare command line interface
parser = argparse.ArgumentParser(description='Export Jupyter Notebooks as Python scripts.')
parser.add_argument('notebook_path', type=str, help="Path of the Jupyter notebook.")
parser.add_argument('output_path', type=str, help="Path of the output script.")
parser.add_argument('--delete_export_comments', '-dc', action='store_true',
                    help="If exists, then #export comments will be deleted from output script.")
#  TODO: Add default value
parser.add_argument('--cell-seperator', '-cs', help='String that seperates exported cells.Default to 2 newlines.')


def run_export_console_script():
    """
    Run export() function from command line.
    """

    #  Parse command line arguments
    args = parser.parse_args(args=sys.argv[1:])
    try:
        export(args.notebook_path, args.output_path, args.delete_export_comments, args.cell_seperator)
    except FileNotFoundError as e:
        print(f"Notebook file not found. {e} not exists.")
