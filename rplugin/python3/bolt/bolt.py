# ============================================================================
# FILE: bolt.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import os
from bolt.explorer import explorer
from bolt.searcher import searcher


class bolt(object):
    """ Main class for the plugin, manages
        the input commands and the spawning of
        explorers """
    def __init__(self):
        # Start in CWD
        cwd = os.path.abspath(os.getcwd())
        self.commanders = {}
        # Create explorers
        self.commanders['exp1'] = explorer(cwd)
        self.commanders['exp2'] = explorer(cwd)
        # Create searchers
        self.commanders['sea1'] = searcher()
        self.commanders['sea2'] = searcher()

# ============================================================================
# Bolt Commands
# ============================================================================
    # commander is used to lookup which object to use from the dict;
    # exp1, exp2, sea1, sea2

    # ==========================================
    # Generic (explorer or searcher) commands
    # ==========================================
    def updateListing(self, pattern, commander):
        pass

    def getSelectedFile(self, commander):
        pass

    def changeSelection(self, offset, commander):
        pass

    def getListing(self, commander):
        pass

    # ==========================================
    # Searcher exclusive commands
    # ==========================================
    def search(self, filePattern, inputPattern,
               fromCommander, commander):
        pass

    # ==========================================
    # Explorer exclusive commands
    # ==========================================
    def move(self, dest, commander):
        pass

    def delete(self, commander):
        pass

    def rename(self, commander):
        pass

    def copy(self, dest, commander):
        pass

    def mkdir(self, name, commander):
        pass

    def createFile(self, name, commander):
        pass

    # ==========================================
    # Explorer to explorer commands
    # ==========================================
    def eToe_copy(self, commander):
        pass

    def eToe_Move(self, commander):
        pass
