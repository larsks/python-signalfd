'''Python support for signalfd(2)

This module provides access to the signalfd(2) system call and the
necessary support operations, including the sigsetops(3) operations and the
sigprocmask(2) system call.

Example usage::

    import sys
    import signal
    import select
    from signalfd import signalfd, sigset

    # Create a signal mask containing all signals.
    mask = sigset()
    mask.fill()

    with signalfd(mask) as fd:
        poll = select.poll()
        poll.register(fd,  select.POLLIN)
        poll.register(sys.stdin, select.POLLIN)

        # Print signals as they are received.  Exit on
        # user pressing <RETURN>.
        while True:
            events = dict(poll.poll())

            if fd.fileno() in events:
                info = fd.info()
                print 'received signal %d' % info.ssi_signo

            if sys.stdin.fileno() in events:
                print 'all done'
                break

'''

from .signalfd import signalfd
from .sigset import sigset, sigprocmask
from .constants import *

