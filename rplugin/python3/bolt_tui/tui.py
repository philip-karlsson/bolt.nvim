import dummy_pane

class tui(object):
    panes = []

    def __init__(self):
        self.panes.append(dummy_pane.dummy_pane(focused=True))
        self.panes.append(dummy_pane.dummy_pane(focused=False))

        self.selected = 0

    def cmd_up(self):
        self.panes[self.selected].cmd_up()

    def cmd_down(self):
        self.panes[self.selected].cmd_down()

    def cmd_tab(self):
        self.panes[self.selected].set_focus(False)
        self.selected = (self.selected + 1) % 2
        self.panes[self.selected].set_focus(True)

    def get_panes(self):
        left = self.panes[0].get_pane()
        right = self.panes[1].get_pane()

        buf = []

        for i in range(0, len(left)):
            str = left[i] + ' | ' + right[i]
            buf.append(str)

        return buf
