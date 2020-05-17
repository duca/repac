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

class Installed:

    def __init__(self, name=None):
        self.name = name
        self.local = '/var/lib/pacman/local'

    def find(self):
        pass

    def rawList(self):
        import os
        self.dirs = []
        self.dirs = os.listdir(self.local)
        return self.dirs

    def pathList(self):
        import os.path
        self.paths = []
        dirs = self.rawList()
        for dir in dirs:
            self.paths.append(os.path.join(self.local, dir))

        return self.paths


    def list(self):
        import os.path
        self.rawList()
        cleaned = []
        for dir in self.dirs:
            path = os.path.join(self.local,dir)
            descFile = os.path.join(path, 'desc')
            desc = open(descFile)
            dum = desc.seek(7)
            cleaned.append(desc.readline().split('\n')[0])
            desc.close()
        return cleaned


if __name__ == '__main__':
    ins = Installed()

    print(ins.list())
    print(ins.rawList())
