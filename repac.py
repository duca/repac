#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#       repac
#       
#       Copyright 2012 Eduardo Martins Lopes <edumloeps@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#  
arglist = {'destination': None, 'verbose':False } 
def main():    
    import installed, package
    import sys
    ins = installed.installed()
    
    dest = arglist["destination"]
    
    #analyse arguments
    arguments(sys.argv)
    completeList = ins.pathList()
    if(arglist['verbose']):
        print("Repackaging:")
    for item in completeList:
        
        if(arglist['verbose']):
            print(item.strip(ins.local))
        pk= package.package(item,arglist["destination"])
        pk.make()

def arguments(items):
    from sys import exit
    for i in range(0,len(items)):
        arg = items[i]
        
        if arg == '-p':
            arglist["destination"] = items[i+1]
        if arg == '-v':
            arglist['verbose']=True
        if arg == '-h':
            stopExec()
            exit()
def stopExec():
    import sys
    sys.stdout.write('''
Repac will generate a .pkg.tar.gz from all your installed packages

Options are: 
-p \t complete path (example /home/user/packages)
-v \t verbose mode
-h \t this message
''')
        
if __name__ == "__main__":
    main()