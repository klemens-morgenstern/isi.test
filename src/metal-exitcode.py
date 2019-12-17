import sys
import gdb
from gdb.FrameDecorator import FrameDecorator


exit_code = None

class exit_stub(gdb.Breakpoint):
    def __init__(self):
        gdb.Breakpoint.__init__(self, "_exit")

    def stop(self):

        frame = gdb.selected_frame()
        args = [arg for arg in frame.block() if arg.is_argument]

        for arg in args:
            exit_code = arg.value(frame)
            break

        gdb.post_event(lambda : self.exit(exit_code))

    def exit(self, exit_code):
        sys.stdout.write("***metal-newlib*** Log: Invoking _exit with {}\n".format(exit_code))
        gdb.execute("set confirm off")
        gdb.execute("quit {}".format(exit_code))


_exit = exit_stub()


def exit_event(event):
    if hasattr(event, 'exit_code') and exit_code:
        gdb.execute("quit {}".format(exit_code))


gdb.events.exited.connect(exit_event)