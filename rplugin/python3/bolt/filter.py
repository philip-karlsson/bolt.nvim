# ============================================================================
# FILE: filter.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import re


class filter(object):
    def __init__(self):
        pass

    def __search(self, input, pattern, output):
        for entry in input[:]:
            res = re.search(pattern, entry, re.IGNORECASE)
            if res is not None:
                output.append(entry)
                input.remove(entry)

    def filter(self, input, pattern, output):
        # Setup patterns for the search
        beginningString = '^' + pattern + '.*'
        wholeString = '.*' + pattern + '.*'
        fuzzy = '.*'
        for c in pattern:
            fuzzy += c + '.*'
        # Perform the search
        c_currentFiles = []
        c_currentFiles[:] = input[:]
        output[:] = []
        self.__search(c_currentFiles, beginningString, output)
        self.__search(c_currentFiles, wholeString, output)
        self.__search(c_currentFiles, fuzzy, output)
