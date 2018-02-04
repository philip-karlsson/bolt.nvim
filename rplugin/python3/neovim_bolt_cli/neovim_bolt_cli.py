# ============================================================================
# FILE: neovim_bolt_cli.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import os
import shutil
from bolt_tui.bolt_tui import bolt_tui

from vim_tc_explorer.filter import filter


class neovim_bolt_cli(object):
    """ Main class for the plugin, manages
        the input commands and the spawning of
        explorers """
    def __init__(self, nvim, log=False):
        self.nvim = nvim
        # Start the explorer in cwd
        self.cwd = os.path.abspath(os.getcwd())
        # Instantiate bolt through the CLI
        self.bolt = bolt_tui(self.cwd)
        # FIXME Move below to the bolt class
        # Create both explorers but only show one depending on cmd?
        self.explorers = []
        self.explorers.append(explorer(self.cwd))
        self.explorers.append(explorer(self.cwd))
        # Index to keep track of which explorer that is currently selected
        self.selectedExplorer = 0

# ============================================================================
# Helpers
# ============================================================================
    def bufCmd(self, buffer, cmd):
        prevbuffer = self.nvim.current.buffer
        self.nvim.current.buffer = buffer
        self.nvim.command(cmd)
        self.nvim.current.buffer = prevbuffer

    def winCmd(self, window, cmd):
        prevwindow = self.nvim.current.window
        self.nvim.current.window = window
        self.nvim.command(cmd)
        self.nvim.current.window = prevwindow

    def close(self, withFile=True):
        # Method used to close the plugin
        # Delete both buffers
        self.nvim.command('stopinsert')
        if(withFile is False):
            # Shift to the OG buffer
            self.nvim.current.buffer = self.ogBuffer
        self.nvim.command('bd %s' % self.explorerBufferNumberOne)
        if(self.explorerBufferNumberTwo is not None):
            self.nvim.command('bd %s' % self.explorerBufferNumberTwo)
        self.nvim.command('bd %s' % self.inputBufferNumber)

    def createKeyMap(self):
        # Remap keys for the input layer
        # Enter
        self.nvim.command("inoremap <buffer> <CR> <ESC>:TcExpEnter<CR>")
        # Backspace
        self.nvim.command("inoremap <buffer> <BS> %")
        # Up
        self.nvim.command("inoremap <buffer> <C-k> <ESC>:TcExpUp<CR>")
        self.nvim.command("inoremap <buffer> <Up> <ESC>:TcExpUp<CR>")
        # Down
        self.nvim.command("inoremap <buffer> <C-j> <ESC>:TcExpDown<CR>")
        self.nvim.command("inoremap <buffer> <Down> <ESC>:TcExpDown<CR>")
        # Tab
        self.nvim.command("inoremap <buffer> <tab> <ESC>:TcExpTab<CR>")
        # Search
        str = "inoremap <buffer> <C-f> <ESC>:TcSearch (-t/-g)file;(pattern): "
        self.nvim.command(str)
        # Set cwd
        self.nvim.command("inoremap <buffer> <C-s> <ESC>:TcSetCwd<CR>")
        # Expand/Collapse search matches
        self.nvim.command("inoremap <buffer> <C-a> <ESC>:TcSearchToggle<CR>")
        # File operations
        #
        # Original total commander shortcuts 
        # F1 - Help
        # F2 - Refresh (suggest to map it to rename)
        # F3 - List file content
        # F4 - Edit
        # F5 - Copy
        # F6 - Move
        # F7 - Create directory
        # F8 - Delete file
        self.nvim.command("inoremap <buffer> <F2> <ESC>:BoltRename name: ")
        self.nvim.command("inoremap <buffer> <F5> <ESC>:BoltCopy dest: ")
        self.nvim.command("inoremap <buffer> <F6> <ESC>:BoltMove name: ")
        self.nvim.command("inoremap <buffer> <F7> <ESC>:BoltMkdir name: ")
        self.nvim.command("inoremap <buffer> <F8> <ESC>:BoltDelete Delete? ")

        remapStr = "inoremap <buffer> <C-p> <ESC>:BoltCreateFile name: "
        self.nvim.command(remapStr)
        # Close
        self.nvim.command("inoremap <buffer> <C-q> <ESC>:TcExpClose<CR>")

# ============================================================================
# Commands
# ============================================================================
    def tc_explore(self, args, range):
        """ Single pane explorer """
        self.numExplorers = 1
        self.selectedExplorer = 0
        # Remember the OG buffer
        self.ogBuffer = self.nvim.current.buffer
        # Create the input buffer
        self.nvim.command('e TC_Input')
        self.nvim.command('setlocal buftype=nofile')
        self.nvim.command('setlocal filetype=vim_tc_input')
        # Might be wrong bcz ref
        self.inputBufferNumber = self.nvim.current.buffer.number

        # Create the explorer buffer
        self.nvim.command('split TC_Explorer')
        self.nvim.command('setlocal buftype=nofile')
        self.nvim.command('setlocal filetype=vim_tc_explorer')
        self.explorerBufferNumberOne = self.nvim.current.buffer.number
        self.explorerWindowOne = self.nvim.current.window
        # Only one explorer
        self.explorerBufferNumberTwo = None
        exp = self.explorers[self.selectedExplorer]
        exp.assignBuffer(self.nvim.buffers[self.explorerBufferNumberOne])
        exp.window = self.nvim.current.window
        # Go back to the input buffer window
        self.nvim.command('wincmd j')
        # FIXME: Add one more line for quick help
        self.nvim.current.window.height = 1
        # Change to input buffer
        self.nvim.current.buffer = self.nvim.buffers[self.inputBufferNumber]
        self.nvim.command("startinsert!")
        self.createKeyMap()
        # Draw first frame
        self.explorers[self.selectedExplorer].draw()

    def tc_explore_dual(self, args, range):
        """ Single pane explorer """
        self.numExplorers = 2
        self.selectedExplorer = 0
        # Remember the OG buffer
        self.ogBuffer = self.nvim.current.buffer
        # Create the input buffer
        self.nvim.command('e TC_Input')
        self.nvim.command('setlocal buftype=nofile')
        self.nvim.command('setlocal filetype=vim_tc_input')
        # Might be wrong bcz ref
        self.inputBufferNumber = self.nvim.current.buffer.number

        # Create the explorer buffers
        self.nvim.command('split TC_Explorer_2')  # 2 Bcz split, (inverted)
        self.nvim.command('setlocal buftype=nofile')
        self.nvim.command('setlocal filetype=vim_tc_explorer')
        self.explorerBufferNumberOne = self.nvim.current.buffer.number
        exp = self.explorers[0]
        exp.window = self.nvim.current.window
        exp.assignBuffer(self.nvim.buffers[self.explorerBufferNumberOne])
        # Two explorers
        self.nvim.command('vsplit TC_Explorer_1')
        self.nvim.command('setlocal buftype=nofile')
        self.nvim.command('setlocal filetype=vim_tc_explorer')
        self.explorerBufferNumberTwo = self.nvim.current.buffer.number
        exp = self.explorers[1]
        exp.window = self.nvim.current.window
        exp.assignBuffer(self.nvim.buffers[self.explorerBufferNumberTwo])
        # Go back to the input buffer window
        self.nvim.command('wincmd j')
        # FIXME: Add one more line for quick help
        self.nvim.current.window.height = 1
        # Change to input buffer
        self.nvim.current.buffer = self.nvim.buffers[self.inputBufferNumber]
        self.nvim.command("startinsert!")
        self.createKeyMap()
        # Draw first frame
        self.explorers[0].active = True
        self.explorers[1].active = False
        self.explorers[0].draw()
        self.explorers[1].draw()

# ============================================================================
# Handlers
# ============================================================================
    def tc_enter(self, args, range):
        # Handle enter
        exp = self.explorers[self.selectedExplorer]
        selFile, lineNum = exp.getSelected()
        if os.path.isdir(os.path.join(exp.cwd,
                         selFile)):
            exp.cd(selFile)
            exp.draw()
            # Clear the line
            self.nvim.current.line = ''
            self.nvim.command('startinsert')
        else:
            filePath = os.path.join(exp.cwd, selFile)
            if(lineNum is not None):
                # Would be nice to go to zz at the same time
                self.nvim.command('e +%d %s' % (lineNum,
                                                os.path.abspath(filePath)))
            else:
                self.nvim.command('e %s' % os.path.abspath(filePath))
            self.close()
            return

    def tc_up(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        exp.changeSelection(-1)
        exp.draw()
        exp.window.cursor = (exp.selected + exp.headerLength, 0)
        self.winCmd(exp.window, 'normal! zz')
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')

    def tc_down(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        exp.changeSelection(1)
        exp.draw()
        exp.window.cursor = (exp.selected + exp.headerLength, 0)
        self.winCmd(exp.window, 'normal! zz')
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')

    def tc_tab(self, args, range):
        # Change focus when having multiple panes
        if(self.numExplorers > 1):
            if(self.selectedExplorer == 1):
                self.selectedExplorer = 0
                self.explorers[0].active = True
                self.explorers[1].active = False
            else:
                self.selectedExplorer = 1
                self.explorers[0].active = False
                self.explorers[1].active = True
            self.explorers[0].draw()
            self.explorers[1].draw()
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')

    def tc_close(self, args, range):
        self.close()

    def tc_set_cwd(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        self.nvim.command("cd %s" % exp.cwd)
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')

    def tc_search(self, args, range):
        """ Search patterns comes from command line """
        # Save the current explorer for restoration when the searcher finish
        self.expSave = self.explorers[self.selectedExplorer]
        # Replace the current explorer with a searcher and borrow its buffer
        se = searcher(self.nvim, self.expSave.buffer, self.expSave.cwd)
        se.window = self.expSave.window
        # Perfor the search with the correct parameters
        dir = self.expSave.cwd
        filePattern = args[1]
        if(len(args) > 2):
            inputPattern = args[2]
        else:
            inputPattern = ''
        se.search(dir, filePattern, inputPattern)
        self.explorers[self.selectedExplorer] = se
        self.explorers[self.selectedExplorer].draw()
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')

    def tc_search_toggle(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        if(exp.isSearcher):
            exp.toggle()
            exp.updateListing(self.nvim.current.line)
            exp.draw()
            self.winCmd(exp.window, 'normal! zz')
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')

    def move(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        exp.move(args[1])
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')
        exp.draw()

    def delete(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        exp.delete(args[1])
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')
        exp.draw()

    def rename(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        exp.rename(args[1])
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')
        exp.draw()

    def copy(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        exp.copy(args[1])
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')
        exp.draw()

    def mkdir(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        exp.mkdir(args[1])
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')
        exp.draw()

    def createFile(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        exp.createFile(args[1])
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')
        exp.draw()

    def handle_input(self):
        """ Input handler for filter """
        exp = self.explorers[self.selectedExplorer]
        inputLine = self.nvim.current.line
        # Check for backspace
        if inputLine.endswith('%'):
            inputLine = inputLine.replace("%", "")
            # Handle backspace
            if not inputLine:
                if(exp.isSearcher):
                    # Restore
                    self.explorers[self.selectedExplorer] = self.expSave
                    exp = self.explorers[self.selectedExplorer]
                    prevbuffer = self.nvim.current.buffer
                    self.nvim.current.buffer = exp.buffer
                    self.nvim.command('setlocal filetype=vim_tc_explorer')
                    self.nvim.current.buffer = prevbuffer
                else:
                    # Change directory to the parrent
                    exp.cd('..')
            inputLine = inputLine[:-1]
        # FIXME: These matches shall be commands instead, just like for "enter"
        elif inputLine.endswith('!'):
            inputLine = inputLine.replace("!", "")
            # Handle selection up
            exp.changeSelection(-1)
        elif inputLine.endswith('@'):
            inputLine = inputLine.replace("@", "")
            # Handle selection down
            exp.changeSelection(1)
        elif inputLine.endswith('?'):
            # Close
            self.close(False)
            return
        self.nvim.current.line = inputLine
        exp.updateListing(inputLine)
        # Draw
        exp.draw()

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
        # The header takes up 9 rows
        self.headerLength = 9

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
