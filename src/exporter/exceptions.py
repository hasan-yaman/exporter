class StyleNotFoundError(Exception):
    def __init__(self, style):
        self.style = style

    def __repr__(self):
        return f"{self.style} not found in installed styles."


class UnsupportedFileError(Exception):
    def __init__(self, file):
        self.file = file

    def __repr__(self):
        return f"Extension of {self.file} is not supported. Supported extensions are: .py and .ipynb"


class UnsupportedImageExtensionError(Exception):
    def __init__(self, extension):
        self.extension = extension

    def __repr__(self):
        return f"Image extension {self.extension} is not supported. Supported extensions are .jpeg, .jpg, .bmp and .png"
