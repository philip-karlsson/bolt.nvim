# ============================================================================
# FILE: vim_tc_explorer.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import neovim
import os
import re
from vim_tc_explorer.copy import CopyUtilitiy
from vim_tc_explorer.logger import log, log_list
from vim_tc_explorer.explorer import explorer
from vim_tc_explorer.searcher import searcher
from vim_tc_explorer.utils import init_utils, python_input


class vim_tc_explorer(object):
    """ Main class for the plugin, manages
        the input commands and the spawning of
        explorers """
    def __init__(self, nvim):
        self.nvim = nvim
        init_utils(nvim)
        self.copyUtil = CopyUtilitiy(nvim)
        # Start the explorer in cwd
        self.cwd = os.path.abspath(os.getcwd())
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
        self.nvim.command('bwipeout %s' % self.explorerBufferNumberOne)
        if(self.explorerBufferNumberTwo is not None):
            self.nvim.command('bwipeout %s' % self.explorerBufferNumberTwo)
        self.nvim.command('bwipeout %s' % self.inputBufferNumber)

    def createKeyMap(self):
        # Remap keys for the input layer
        # Enter
        self.nvim.command("inoremap <buffer> <CR> <ESC>:BoltExpEnter<CR>")
        self.nvim.command("inoremap <buffer> <C-j> <ESC>:BoltExpEnter<CR>")
        # Backspace
        self.nvim.command("inoremap <buffer> <BS> %")
        self.nvim.command("inoremap <buffer> <C-h> %")
        # Up
        self.nvim.command("inoremap <buffer> <Up> <ESC>:BoltExpUp<CR>")
        self.nvim.command("inoremap <buffer> <C-p> <ESC>:BoltExpUp<CR>")
        # Down
        self.nvim.command("inoremap <buffer> <Down> <ESC>:BoltExpDown<CR>")
        self.nvim.command("inoremap <buffer> <C-n> <ESC>:BoltExpDown<CR>")
        # Pg Up
        self.nvim.command("inoremap <buffer> <C-u> <ESC>:BoltPgUp<CR>")
        # Pg Down
        self.nvim.command("inoremap <buffer> <C-d> <ESC>:BoltPgDown<CR>")
        # Tab
        self.nvim.command("inoremap <buffer> <tab> <ESC>:BoltExpTab<CR>")
        # Search
        str = "inoremap <buffer> <C-b> <ESC>:BoltSearch (-t/-g)file;(pattern): "
        self.nvim.command(str)
        # Find
        str = "inoremap <buffer> <C-f> <ESC>:BoltFind "
        self.nvim.command(str)
        # Grep
        str = "inoremap <buffer> <C-g> <ESC>:BoltGrep "
        self.nvim.command(str)
        # Git status
        str = "inoremap <buffer> <C-i> <ESC>:BoltGitStatus<CR>"
        self.nvim.command(str)
        # Abort filter
        str = "inoremap <buffer> <C-w> <ESC>:BoltAbortFilter<CR>"
        self.nvim.command(str)
        # Set cwd
        self.nvim.command("inoremap <buffer> <C-s> <ESC>:BoltSetCwd<CR>")
        # Expand/Collapse search matches
        self.nvim.command("inoremap <buffer> <C-a> <ESC>:BoltSearchToggle<CR>")
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
        self.nvim.command("inoremap <buffer> <C-c> <ESC>:BoltCopy<CR>")
        self.nvim.command("inoremap <buffer> <C-v> <ESC>:BoltPaste<CR>")
        self.nvim.command("inoremap <buffer> <F6> <ESC>:BoltMove name: ")
        self.nvim.command("inoremap <buffer> <F7> <ESC>:BoltMkdir name: ")
        remapStr = "inoremap <buffer> <F8> <ESC>:BoltDelete<CR>"
        self.nvim.command(remapStr)
        remapStr = "inoremap <buffer> <C-t> <ESC>:BoltCreateFile name: "
        self.nvim.command(remapStr)
        # Close
        self.nvim.command("inoremap <buffer> <C-q> <ESC>:BoltExpClose<CR>")

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
        self.nvim.current.window.height = 2
        # Change to input buffer
        self.nvim.current.buffer = self.nvim.buffers[self.inputBufferNumber]
        self.nvim.command("startinsert!")
        str = 'Help: <kbd> Filter pattern; <bs> Go to parent'
        self.nvim.current.buffer.append(str)
        self.createKeyMap()
        # Draw first frame
        # Refresh the current directory listing first
        if not self.explorers[self.selectedExplorer].isSearcher:
            self.explorers[self.selectedExplorer].refreshListing()
        self.explorers[self.selectedExplorer].updateListing("")
        self.explorers[self.selectedExplorer].draw()

    def tc_explore_cwd(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        exp.cd(self.cwd)
        self.tc_explore(args, range)

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
        self.nvim.current.window.height = 2
        # Change to input buffer
        self.nvim.current.buffer = self.nvim.buffers[self.inputBufferNumber]
        self.nvim.command("startinsert!")
        str = 'Help: <kbd> Filter pattern; <bs> Go to parent'
        self.nvim.current.buffer.append(str)
        self.createKeyMap()
        # Draw first frame
        self.explorers[0].active = True
        self.explorers[1].active = False
        self.explorers[0].updateListing("")
        self.explorers[1].updateListing("")
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
            self.abortFilter(None, None)
        else:
            try:
                filePath = os.path.join(exp.cwd, selFile)
                if(lineNum is not None):
                    # Would be nice to go to zz at the same time
                    self.nvim.command('e +%d %s' % (lineNum,
                                                    os.path.abspath(filePath)))
                else:
                    self.nvim.command('e %s' % os.path.abspath(filePath))
            except neovim.api.nvim.NvimError as err:
                print("Error/possibly warning opening file")
            self.close()
            return

    def tc_up(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        oldSel = exp.selected
        exp.changeSelection(-1)
        exp.window.cursor = (exp.selected + exp.headerLength, 0)
        ind = oldSel + exp.headerLength - 1
        exp.buffer[ind] = exp.buffer[ind].replace("-->", "   ")
        ind = exp.selected + exp.headerLength - 1
        exp.buffer[ind] = exp.buffer[ind].replace("   ", "-->")
        if(exp.selected == 0):
            self.winCmd(exp.window, 'normal! zz')
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')

    def tc_down(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        oldSel = exp.selected
        exp.changeSelection(1)
        exp.window.cursor = (exp.selected + exp.headerLength, 0)
        ind = oldSel + exp.headerLength - 1
        exp.buffer[ind] = exp.buffer[ind].replace("-->", "   ")
        ind = exp.selected + exp.headerLength - 1
        exp.buffer[ind] = exp.buffer[ind].replace("   ", "-->")
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')

    def pg_up(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        oldSel = exp.selected
        exp.changeSelection(-20)
        if(exp.selected == 0):
            self.winCmd(exp.window, 'normal! zz')
        exp.window.cursor = (exp.selected + exp.headerLength, 0)
        ind = oldSel + exp.headerLength - 1
        exp.buffer[ind] = exp.buffer[ind].replace("-->", "   ")
        ind = exp.selected + exp.headerLength - 1
        exp.buffer[ind] = exp.buffer[ind].replace("   ", "-->")
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')

    def pg_down(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        oldSel = exp.selected
        exp.changeSelection(20)
        exp.window.cursor = (exp.selected + exp.headerLength, 0)
        ind = oldSel + exp.headerLength - 1
        exp.buffer[ind] = exp.buffer[ind].replace("-->", "   ")
        ind = exp.selected + exp.headerLength - 1
        exp.buffer[ind] = exp.buffer[ind].replace("   ", "-->")
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
        self.close(False)

    def tc_set_cwd(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        self.cwd = exp.cwd
        self.nvim.command("cd %s" % exp.cwd)
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')

    def tc_find(self, args, range):
        """ The find command """
        # Save the current explorer for restoration when the searcher finish
        self.expSave = self.explorers[self.selectedExplorer]
        # Replace the current explorer with a searcher and borrow its buffer
        se = searcher(self.nvim, self.expSave.buffer, self.expSave.cwd)
        se.window = self.expSave.window
        # Perform the search with the correct parameters
        dir = self.expSave.cwd
        se.find(dir, args[0])
        self.explorers[self.selectedExplorer] = se
        self.explorers[self.selectedExplorer].draw()
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')
        str = 'Help: <kbd> Filter pattern; <bs> Go to parent'
        self.nvim.current.buffer.append(str)

    def tc_grep(self, args, range):
        """ The grep command """
        # Save the current explorer for restoration when the searcher finish
        self.expSave = self.explorers[self.selectedExplorer]
        # Replace the current explorer with a searcher and borrow its buffer
        se = searcher(self.nvim, self.expSave.buffer, self.expSave.cwd)
        se.window = self.expSave.window
        # Perform the search with the correct parameters
        dir = self.expSave.cwd
        filePattern = ""
        if(len(args) > 1):
            filePattern = args[0]
            pattern = args[1]
        else:
            pattern = args[0]
        se.grep(dir, filePattern, pattern)
        self.explorers[self.selectedExplorer] = se
        self.explorers[self.selectedExplorer].draw()
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')
        str = 'Help: <kbd> Filter pattern; <bs> Go to parent'
        self.nvim.current.buffer.append(str)

    def gitStatus(self, args, range):
        firstFile = self.explorers[self.selectedExplorer].getFirstFile()
        filePath = os.path.join(self.explorers[self.selectedExplorer].cwd, firstFile)
        self.nvim.command('e %s' % (os.path.abspath(filePath)))
        self.close()
        self.nvim.command('G')
        self.nvim.command('bwipeout #')

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
        str = 'Help: <kbd> Filter pattern; <bs> Go to parent'
        self.nvim.current.buffer.append(str)

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
        exp.delete()
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')
        exp.draw()

    def toggleMark(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        if exp.isMarked(exp.fileredFiles[exp.selected]):
            exp.removeMarker(exp.selected)
        else:
            exp.addMarker(exp.selected)
        exp.draw()

    def rename(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        exp.rename(args[1])
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')
        exp.draw()

    def cut(self, args, range):
        log('cut')
        # Get the selected files to clipboard
        exp = self.explorers[self.selectedExplorer]
        cb = exp.get_markers_as_string()
        # This way it is consistent between different instances
        # of bolt => will be nice for the refactoring of
        # multiple panes :)
        # Add operation type (copy/move) as prefix
        self.nvim.command("let g:BoltCb = '%s'" % ('mv#' + cb))
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')

    def copy(self, args, range):
        log('copy')
        # Get the selected files to clipboard
        exp = self.explorers[self.selectedExplorer]
        cb = exp.get_markers_as_string()
        # Add the path(s) to bolt ('b') register
        self.nvim.command("let @b='%s'" % (cb.replace('_{%boltSplitter%}_', ',')))
        # This way it is consistent between different instances
        # of bolt => will be nice for the refactoring of
        # multiple panes :)
        # Add operation type (copy/move) as prefix
        self.nvim.command("let g:BoltCb = '%s'" % ('cp#' + cb))
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')

    def paste(self, args, range):
        exp = self.explorers[self.selectedExplorer]
        rawCb = self.nvim.command_output('silent echo g:BoltCb')
        rawCb = rawCb.strip('\n')
        # Get opcode
        p = re.compile('^(.*?)\#')
        op = p.findall(rawCb)[0]
        rawCb = re.sub(r'^.*\#', '', rawCb)
        # Parse the raw clipboard and recreate the list
        cb = rawCb.split('_{%boltSplitter%}_')
        if op == 'cp':
            self.copyUtil.copy_list(cb, exp.cwd)
        elif op == 'mv':
            self.copyUtil.move_list(cb, exp.cwd)
        exp.refreshListing()
        exp.updateListing(exp.pattern)
        exp.draw()
        self.nvim.command('startinsert')
        self.nvim.command('normal! $')

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
        # Set the new file as selected
        exp.setSelectionWithName(args[1])
        exp.draw()
        self.tc_enter(None, None)

    def abortFilter(self, args, range):
        str = 'Help: <kbd> Filter pattern; <bs> Go to parent'
        self.nvim.current.buffer[1] = str
        self.nvim.current.buffer[0] = ""
        self.nvim.command('startinsert')
        exp = self.explorers[self.selectedExplorer]
        exp.updateListing("")
        exp.draw()

    def handle_input(self):
        """ Input handler for filter """
        exp = self.explorers[self.selectedExplorer]
        inputLine = self.nvim.current.line
        # Handle space for the markers
        if inputLine == " ":
            self.nvim.current.line = ""
            self.toggleMark(None, None)
            self.tc_down(None, None)
            return
        elif inputLine.endswith(" "):
            self.toggleMark(None, None)
            self.tc_down(None, None)
            withoutSpace = self.nvim.current.line[:-1]
            self.nvim.current.line = withoutSpace
            return

        if(inputLine is not "" and inputLine is not "%"):
            self.nvim.current.buffer[1] = 'Filter active: (abort with <c-w>)'
        # Check for backspace
        if inputLine.endswith('%'):
            inputLine = inputLine.replace("%", "")
            # Handle backspace
            if not inputLine and (not self.nvim.current.buffer[1] ==
                                  'Filter active: (abort with <c-w>)'):
                if(exp.isSearcher):
                    # Restore
                    self.expSave.window = exp.window
                    self.explorers[self.selectedExplorer] = self.expSave
                    exp = self.explorers[self.selectedExplorer]
                    prevbuffer = self.nvim.current.buffer
                    self.nvim.current.buffer = exp.buffer
                    self.nvim.command('setlocal filetype=vim_tc_explorer')
                    self.nvim.current.buffer = prevbuffer
                    str = 'Help: <kbd> Filter pattern; <bs> Go to parent'
                    self.nvim.current.buffer.append(str)
                else:
                    # Change directory to the parrent
                    exp.cd('..')
            inputLine = inputLine[:-1]
        # Check if we still have matches
        if(0 == exp.updateListing(inputLine)):
            inputLine = inputLine[:-1]
        self.nvim.current.line = inputLine
        # Draw
        exp.selected = 0
        exp.draw()
        if(len(exp.fileredFiles) != 0):
            exp.window.cursor = (exp.selected + exp.headerLength, 0)
