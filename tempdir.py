import tempfile
import os
class TempDir(object):
    """ class for temporary directories
creates a (named) directory which is deleted after use.
All files created within the directory are destroyed
Might not work on windows when the files are still opened
"""
    def __init__(self, suffix="", prefix="tmp", dir=None):
        self.name=tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=dir)

    def __del__(self):
        if "name" in self.__dict__:
            self.__exit__(None, None, None)

    def __enter__(self):
        return self

    def __exit__(self, *errstuff):
        return self.dissolve()

    def dissolve(self):
        if self.name:
            for (dir, dirs, files) in os.walk(self.name, topdown=False):
                for f in files:
                    os.unlink(os.path.join(dir, f))
                os.rmdir(dir)
        self.name = ""

    def __str__(self):
        if self.name:
            return "temporary directory at: %s"%(self.name,)
        else:
            return "dissolved temporary directory"


