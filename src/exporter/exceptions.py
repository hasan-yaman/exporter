class StyleNotFoundError(Exception):
    def __init__(self, style):
        self.style = style

    def __repr__(self):
        return f"{self.style} not found in installed styles."


class UnsupportedFileError(Exception):
    def __init__(self, file):
        self.file = file

    def __repr__(self):
        return f"Extension of {self.file} is not supported. Support extensions are: .py and .ipynb"