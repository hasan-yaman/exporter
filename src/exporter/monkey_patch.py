import io
import codecs

old_open = codecs.open


class MemoryFile:
    def __init__(self, buffer):
        self.buffer = buffer

    def read(self, size=-1):
        return self.buffer.read(size)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.buffer.close()


#  imgkit uses codecs to read css file. codecs.open function opens file and reads it.
#  For the project, we need to read css data directly from string. That's why we are monkey patching
#  codecs.open function. To handle reading from in memory string.
def patched_open(filename, mode='r', encoding=None, errors='strict', buffering=1):
    if isinstance(filename, io.StringIO):
        return MemoryFile(filename)
    else:
        return old_open(filename, mode, encoding, errors, buffering)
