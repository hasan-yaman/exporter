import sys
import argparse
from .exporter import export
from .image_exporter import image_export, available_styles
from .exceptions import *

# Prepare command line interface
export_parser = argparse.ArgumentParser(description='Export Jupyter Notebooks as Python scripts.')
export_parser.add_argument('notebook_path', type=str, help="Path of the Jupyter notebook.")
export_parser.add_argument('output_path', type=str, help="Path of the output script.")
export_parser.add_argument('--delete-export-comments', '-dc', action='store_true',
                           help="If exists, then #export comments will be deleted from output script.")
export_parser.add_argument('--cell-seperator', '-cs', action='store', default="\n\n",
                           help='String that seperates exported cells.Default to 2 newlines.')

image_export_parser = argparse.ArgumentParser(description="Export Python scripts or Jupyter Notebooks as an image.")
image_export_parser.add_argument('input_path', nargs='?', type=str, help="Path of the input file.")
image_export_parser.add_argument('output_path', nargs='?', type=str, help="Output path of the exported image.")
image_export_parser.add_argument('style', nargs='?', type=str, help="Style of the output image.")
image_export_parser.add_argument('--zoom', '-z', type=float, default=2.0, help="Zoom level of the output image.")
image_export_parser.add_argument('--styles', '-s', action='store_true',
                                 help="List all the available styles.")


def run_export_console_script():
    """
    Run export() function from command line.
    """

    #  Parse command line arguments
    args = export_parser.parse_args(args=sys.argv[1:])
    print(args.notebook_path, args.output_path, args.delete_export_comments, args.cell_seperator)
    try:
        export(args.notebook_path, args.output_path, args.delete_export_comments, args.cell_seperator)
    except FileNotFoundError as e:
        print(f"Notebook file not found. {e} not exists.")
    except UnsupportedFileExtensionError as e:
        print(f"Extension of {e} is not supported.")


def run_image_export_console_script():
    """
    Run image_export() or get_all_styles() functions from command line.
    """
    args = image_export_parser.parse_args(args=sys.argv[1:])
    if args.styles:
        print(available_styles())
    else:
        #  To use --styles with positional arguments, we pass n_args='?' to add_argument() for positional
        #  arguments. Therefore, we need to check whether positional arguments are None or not.
        if args.input_path is None:
            image_export_parser.error("the following arguments are required: input_path, output_path, style")
        else:
            if args.output_path is None:
                image_export_parser.error("the following arguments are required: output_path, style")
            else:
                if args.style is None:
                    image_export_parser.error("the following arguments are required: style")
        try:
            image_export(args.input_path, args.output_path, args.style, args.zoom)
        except FileNotFoundError as e:
            print(f"File not found. {e} not exists.")
        except StyleNotFoundError as e:
            print(f"{e} not found in installed styles.")
        except UnsupportedFileExtensionError as e:
            print(f"Extension of {e} is not supported.")
