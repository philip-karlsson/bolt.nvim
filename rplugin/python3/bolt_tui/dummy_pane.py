class dummy_pane(object):
    current_line = 0

    buffer = ['file1','file2','file3','file4']

    def __init__(self, focused=False):
        self.focused = focused

    def cmd_up(self):
        self.current_line = max(0, self.current_line-1)

    def cmd_down(self):
        self.current_line = min(len(self.buffer)-1, self.current_line+1)

    def set_focus(self, focused):
        self.focused = focused

    def get_pane(self):
        buf = []
        for i in range(0, len(self.buffer)):
            if self.current_line == i and self.focused:
                str = '--> '
            else:
                str = '    '
            str += self.buffer[i]
            buf.append(str)

        return buf
