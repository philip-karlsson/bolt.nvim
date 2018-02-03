# ============================================================================
# FILE: explorer.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import os
import shutil
from vim_tc_explorer.filter import filter


class explorer(object):
    """ Class for an explorer that is used in the panes """
    def __init__(self, cwd):
        self.isSearcher = False
        # Instance of the filter
        self.filter = filter()
        self.cwd = cwd
        # The the current files
        self.currentFiles = os.listdir(self.cwd)
        self.fileredFiles = self.currentFiles[:]
        # Index that tracks which file that is selected
        self.selected = 0
        self.active = True
        self.pattern = ''

    def assignBuffer(self, buffer):
        self.buffer = buffer

    def draw(self):
        explorer = self.buffer
        # New way of getting the header
        explorer[:] = self.getUIHeader()
        # FIXME: Add coloring
        for idx, val in enumerate(self.fileredFiles):
            if idx == self.selected and self.active:
                token = "-->"
            else:
                token = "   "
            if(os.path.isdir(os.path.abspath(os.path.join(self.cwd, val)))):
                # Folder
                explorer.append(token + ' +' + val + '/')
            else:
                explorer.append(token + '  ' + val)

    def rename(self, newName):
        os.rename(self.getSelected()[0], os.path.join(self.cwd, newName))
        self.cd('.')
        self.updateListing(self.pattern)

    def copy(self, dest):
        selFile = self.getSelected()[0]
        if os.path.isdir(selFile):
            shutil.copytree(selFile, dest)
        else:
            shutil.copy(selFile, dest)
        self.cd('.')
        self.updateListing(self.pattern)

    def delete(self, yesno):
        if yesno == "y":
            selFile = self.getSelected()[0]
            if os.path.isdir(selFile):
                shutil.rmtree(selFile)
            else:
                os.remove(selFile)
            self.cd('.')
            self.updateListing(self.pattern)

    def move(self, dest):
        os.rename(self.getSelected()[0], dest)
        self.cd('.')
        self.updateListing(self.pattern)

    def mkdir(self, name):
        os.makedirs(os.path.join(self.cwd, name))
        self.cd('.')
        self.updateListing(self.pattern)

    def createFile(self, name):
        open(os.path.join(self.cwd, name), 'a').close()
        self.cd('.')
        self.updateListing(self.pattern)

    def cd(self, path):
        self.cwd = os.path.abspath(os.path.join(self.cwd, path))
        self.currentFiles = os.listdir(self.cwd)
        self.fileredFiles = self.currentFiles[:]
        self.changeSelection(0)

    def updateListing(self, pattern):
        self.pattern = pattern
        self.filter.filter(self.currentFiles, pattern, self.fileredFiles)
        self.changeSelection(0)

    def changeSelection(self, offset):
        self.selected += offset
        if self.selected < 0:
            self.selected = 0
        elif self.selected >= len(self.fileredFiles):
            self.selected = len(self.fileredFiles)-1

    def getSelected(self):
        pathToFile = os.path.join(self.cwd, self.fileredFiles[self.selected])
        return pathToFile, None

    # Gui header
    def getUIHeader(self):
        bar = "==============================================================="
        if(self.active):
            leadingC = '# '
        else:
            leadingC = '" '
        ret = []
        ret.append(leadingC + bar)
        ret.append(leadingC + 'Bolt for Neovim (alpha)')
        # Shall be highlighted
        ret.append(leadingC + '  $>' + self.cwd)
        qhStr = '  Quik Help: <Ret>:Open   <C-q>:Quit   <C-s>:Set CWD'
        ret.append(leadingC + qhStr)
        qhStr = '             <C-f>:Search <C-p>:Create File'
        ret.append(leadingC + qhStr)
        qhStr = '             <F2>:Rename  <F5>:Copy    <F6>:Move   '
        ret.append(leadingC + qhStr)
        qhStr = '             <F7>:Mkdir   <F8>:Delete   '
        ret.append(leadingC + qhStr)
        ret.append(leadingC + bar)
        return ret
