# signalfd for Python

This is a [cffi][1] based module for Python that makes available the
`signalfd()` system call, as well as all of `sigsetops(3)`.  The
`signalfd()` calls allows your code to receive signals via a file
descriptor, rather than via the normal asynchronous delivery method,
which makes signals much more compatible with event based solutions
(such as those using `select.select`, `select.poll`, and so forth).

For details, please see the `signalfd(2)` man page.

## Requirements

You will need the [cffi][2] module for Python.

[1]: http://cffi.readthedocs.org/
[2]: https://pypi.python.org/pypi/cffi

## Examples

    import signal
    import select
    from signalfd.sigset import sigset
    from signalfd.signalfd import signalfd

    mask = sigset()
    mask.add(signal.SIGINT)
    mask.add(signal.SIGQUIT)

    with signalfd(mask) as fd:
        poll = select.poll()
        poll.register(fd,  select.POLLIN)

        while True:
            events = dict(poll.poll())

            if fd.fileno() in events:
                info = fd.info()
                print 'received signal %d' % info.ssi_signo

## License

signalfd for Python
Copyright (C) 2013 Lars Kellogg-Stedman <lars@oddbit.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

