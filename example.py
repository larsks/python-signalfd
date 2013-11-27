import sys
import signal
import select
from signalfd import signalfd, sigset

# Create a signal set containing all signals.
mask = sigset()
mask.fill()

with signalfd(mask) as fd:
    poll = select.poll()
    poll.register(fd,  select.POLLIN)
    poll.register(sys.stdin, select.POLLIN)

    # Print signals as they are received until user presses <RETURN>.
    while True:
        events = dict(poll.poll())

        if fd.fileno() in events:
            info = fd.info()
            print 'received signal %d' % info.ssi_signo

        if sys.stdin.fileno() in events:
            print 'all done'
            break

