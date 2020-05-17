#!/usr/bin/python3
# -*- coding: utf-8 -*-

#     repac
#
#     Copyright 2020 Eduardo Martins Lopes <edumloeps@gmail.com>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
