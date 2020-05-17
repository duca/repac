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


arglist = {'destination': None, 'verbose':False, "nthreads": 0}
local = None
def main():
    import installed
    import sys
    from multiprocessing import Pool

    #analyse arguments
    arguments(sys.argv)

    if(arglist['nthreads'] == 0 ):
        nthreads = 1
    else:
        nthreads = arglist['nthreads']

    worker = Pool(nthreads) #set the number of threads within the pool
    ins = installed.Installed()
    dest = arglist["destination"]

    completeList = ins.pathList()
    if(arglist['verbose']):
        string = "\nRepackaging using " + str(nthreads) +" threads \n\t Use the -n option to change number of workers \n"
        print(string)
        local = ins.local
    else:
        string = "\nRepackaging silently using " + str(nthreads) +" threads \n\t Use the -n option to change number of workers \n"
        print(string)

    worker.map(job, completeList)


def job(item):
    import package
    if(arglist['verbose']):
        print(item.strip(local))
    pk= package.Package(item,arglist["destination"])
    pk.make()

def arguments(items):
    from sys import exit
    for i in range(0,len(items)):
        arg = items[i]

        if arg == '-p':
            arglist["destination"] = items[i+1]
        if arg == '-v':
            arglist['verbose']=True
        if arg == '-n':
            arglist['nthreads']=int(items[i+1])
        if arg == '-h':
            stopExec()
            exit()
def stopExec():
    import sys
    sys.stdout.write('''
Repac will generate a .pkg.tar.gz from all your installed packages

Options are:
-p \t complete path (example /home/user/packages)
-n \t int  (number of cores to use)
-v \t verbose mode
-h \t this message
''')

if __name__ == "__main__":
    main()
