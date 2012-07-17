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
#      THIS FILE IS PART OF repac
class package:
    
    """Pacman package class
        v0.0.3
     """
    
    def __init__(self, pkgPath, pkgDest=None):
        import collections, os, tempdir
        
        self.path = pkgPath              
        if(pkgDest == None):
            self.pkgDest= os.getcwd()
        else:
            self.pkgDest = pkgDest

        self.files=[]
        self.install = []
        self.desc = collections.OrderedDict()
        self.descArrays = collections.OrderedDict()        
        self.version = '0.0.3'
        self.desc['pkgname']=  ''
        self.desc['pkgver']= ''
        self.desc['pkgdesc']= ''
        self.desc['url']=''
        self.desc['builddate'] = ''
        self.desc['packager']='Unknown Packager'
        self.desc['arch']='i686'
        self.desc['size'] = 0
        self.desc['license']='GPL'
        self.descArrays['backup'] = []
        self.descArrays['depend'] = []
        self.descArrays['optdepend'] = []
        self.descArrays['conflict'] = []
        self.descArrays['provides'] = []
        self.baselist = {'pkgname':'%NAME%', 'pkgver':'%VERSION%', 'pkgdesc':'%DESC%', 'replaces':'%REPLACES%', 
                     'url':'%URL%', 'license':'%LICENSE%', 'arch':'%ARCH%', 'builddate':'%BUILDDATE%', 
                     'packager':'%PACKAGER%', 'size':'%SIZE%', 'depend':'%DEPENDS%', 'provides':'%PROVIDES%'}
    def make(self):
        import tarfile, bz2, os.path, sys, os
        import tempdir
        #Temporary Directory
        td = tempdir.TempDir()
        tempPath = td.name
        os.chdir(tempPath)
        
        #Parse files
        self.parseDesc()
        self.parseFiles()
        if(self.parseINSTALL()):
            self.createINSTALL()
        
        #Create PKGINFO inside the temporary directory 
        self.createPKGINFO()
        name = self.desc["pkgname"] + "-" + self.desc["pkgver"]+".pkg.tar.bz2"
        completePath = os.path.join(self.pkgDest, name)
        pkg = tarfile.open(completePath, mode="w:bz2", dereference=False)
        for file in self.files:
            try:
                pkg.add(file)
            except:
                string = "Was not able to add the " + file + " of package: " + self.desc['pkgname']+ "\n Please run repac again as root \n"
                sys.stderr.write(string)
                #sys.exit()            
        pkg.close()
        td.dissolve()

    def createPKGINFO(self):
        import os, os.path, sys
        self.pkginfo = open(".PKGINFO",mode='w')
        string = "# Generated by repac v"+ str(self.version) + "\n"
        self.pkginfo.write(string)
        string = "# Written by duca < edumlopes at yahoo.com.br >" + "\n"
        self.pkginfo.write(string)
                
        for item in self.desc:
            try:
                string = str(item) + ' = ' + str(self.desc[item]) + "\n"
                self.pkginfo.write(string)
            except: 
                sys.stderr.write("Could not convert data at package.py line 97")
                #sys.exit()
        
        for item in self.descArrays:
            array = self.descArrays[item]
            if(len(array) > 0):
                for i in range(0,len(array)):
                    try:
                        string = str(item) + ' = '+ str(array[i]) + "\n"
                        self.pkginfo.write(string)
                    except:
                        sys.stderr.write("Could not convert data at package.py line 107")
                        #sys.exit()
        self.pkginfo.close()
    
    def createINSTALL(self):
        import os, os.path, sys
        installFile = open(".INSTALL",mode='w')
        
        for line in self.install:
            installFile.write(line)
        installFile.close()               
        self.files.append(".INSTALL")
                
        
    def parseDesc(self):
        import os.path
        depends = []
        optdepends = []
        conflicts = []
        provides = []
        path = os.path.join(self.path,"desc")
        df = open(path,mode='r')
        content = df.readlines()
        i = 0
        
        for i in range(len(content)):            
            for item in self.desc:
                if(content[i].rfind(self.baselist[item]) >=0):
                    self.desc[item] = content[i+1].strip('\n')                    
            if(content[i].rfind("%DEPENDS%") >= 0):
                k = i+1
                while(self.keyWord(content[k])):
                    depends.append(content[k].strip('\n'))
                    k+=1
                    if(k >= len(content)):
                        break
            if(content[i].rfind("%OPTDEPENDS%") >= 0):
                k = i+1
                while(self.keyWord(content[k])):
                    optdepends.append(content[k].strip('\n'))
                    k+=1
                    if(k >= len(content)):
                        break
            if(content[i].rfind("%CONFLICTS%") >= 0):
                k = i+1
                while(self.keyWord(content[k])):
                    conflicts.append(content[k].strip('\n'))
                    k+=1
                    if(k >= len(content)):
                        break
            if(content[i].rfind("%PROVIDES%") >= 0):
                k = i+1
                while(self.keyWord(content[k])):
                    provides.append(content[k].strip('\n'))
                    k+=1
                    if(k >= len(content)):
                        break
        self.descArrays['depend'] = depends
        self.descArrays['optdepend'] = optdepends
        self.descArrays['conflict'] = conflicts
        self.descArrays['provides'] = provides
    def keyWord(self, word):
        key = True
            
        if(word.rfind("%CONFLICTS%") > -1):
            return False
        elif(word.rfind("%PROVIDES%") > -1):
            return False
        elif(word.rfind("%OPTDEPENDS%") > -1):
            return False
        elif(word.rfind("%DEPENDS%") > -1):
            return False
        elif(word == "\n"):
            return False
        
        return True
        
    def parseINSTALL(self):
        import os.path
        path = os.path.join(self.path,"install")
        installFlag = False        
        try:
            fi = open(path, mode='r')
            self.install= fi.readlines()
            
            installFlag = True
        except:
            installFlag = False
        return installFlag
   
    def parseFiles(self):
        import os.path
        backup = []
        path = os.path.join(self.path,"files")
        ff = open(path,mode='r')        
        content = ff.readlines()
        
        for i in range(1, len(content)):
            content[i] = "/"+content[i].strip('\n')            
        try:
            content.pop(0) #removes the first line
        except:
            pass
        
        for i in range(0,len(content)):
            item = content[i]
            #remove pure directory  entries otherwise the tar file will be imense in some cases
            if(os.path.isdir(item) == False):
                if(item.rfind("BACKUP")>= 0):
                    for j in range(i+1,len(content)):
                        backup.append(item)
                    break
                elif(os.path.isfile(item)):
                    self.files.append(item)
            #If item is a symlink to a directory, add it anyway (usecase lib64 -> lib in glibc)
            elif(os.path.islink(item) == True):
                self.files.append(item)
#        for item in self.files:
#            print(item)
        pkgInfoPath = ".PKGINFO"
        self.files.append(pkgInfoPath)
        self.descArrays["backup"]=backup   
                            
def main():    
    import installed
    ins = installed.installed()
    installedPkgs = ins.pathList()
    
    for i in range(0, len(installedPkgs)):
        if(installedPkgs[i].rfind("mendeley") >= 0):
            pkgIndex = i
            break
    pk= package(installedPkgs[pkgIndex])
    pk.make()
    
if __name__ == '__main__':
    main()
    

