class StyleNotFoundError(Exception):
    def __init__(self, style):
        self.style = style

    def __repr__(self):
        return f"{self.style} not found in installed styles."


class UnsupportedFileExtensionError(Exception):
    def __init__(self, file, supported_extensions):
        self.file = file
        self.supported_extension = ""
        for i, sf in enumerate(supported_extensions):
            self.supported_extension += f"{sf}" if len(supported_extensions) == 1 or i != len(
                supported_extensions) - 1 else f"{sf}, "

    def __repr__(self):
        return f"Extension of {self.file} is not supported. Supported extensions are: {self.supported_extension}"
