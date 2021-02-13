# exporter

exporter is a simple package that helps to export Jupyter notebooks as a Python script.
Add **#export** or **# export** comments anywhere in the notebook cell you want to export as a Python script. Cells in 
the same notebook will be exported to the same Python script.

The best part of the exporter, it will not create any artifacts when you export cells.


# Installation

```
pip install exporter
```

Check [PyPI](https://pypi.org/project/exporter/) for all the versions available.

# Usage

1. Add **#export** or **# export** comments to cells you want to export.
2. 
    1. Option 1: Use command line.
          ```
          exporter notebook_path.ipynb output_path.py
          ```
          For all the options:
          ```
          exporter --help
          ```
    2. Option 2: Use Python function.
          ```python
          from exporter import export
          export("notebook_path.ipynb","oytput_path.py")
          ```


