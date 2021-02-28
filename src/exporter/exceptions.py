class StyleNotFoundError(Exception):
    def __init__(self, style):
        self.style = style

    def __repr__(self):
        return f"{self.style} not found in installed styles."
