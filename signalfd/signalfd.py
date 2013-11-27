#!/usr/bin/python

import os
import sys
import signal

from .common import ffi, crt
from .sigset import sigprocmask
from .constants import *

ffi.cdef('''
struct signalfd_siginfo {
   uint32_t ssi_signo;   /* Signal number */
   int32_t  ssi_errno;   /* Error number (unused) */
   int32_t  ssi_code;    /* Signal code */
   uint32_t ssi_pid;     /* PID of sender */
   uint32_t ssi_uid;     /* Real UID of sender */
   int32_t  ssi_fd;      /* File descriptor (SIGIO) */
   uint32_t ssi_tid;     /* Kernel timer ID (POSIX timers)
   uint32_t ssi_band;    /* Band event (SIGIO) */
   uint32_t ssi_overrun; /* POSIX timer overrun count */
   uint32_t ssi_trapno;  /* Trap number that caused signal */
   int32_t  ssi_status;  /* Exit status or signal (SIGCHLD) */
   int32_t  ssi_int;     /* Integer sent by sigqueue(3) */
   uint64_t ssi_ptr;     /* Pointer sent by sigqueue(3) */
   uint64_t ssi_utime;   /* User CPU time consumed (SIGCHLD) */
   uint64_t ssi_stime;   /* System CPU time consumed (SIGCHLD) */
   uint64_t ssi_addr;    /* Address that generated signal
                            (for hardware-generated signals) */
   uint8_t  pad[48];      /* Pad size to 128 bytes (allow for
                             additional fields in the future) */
};

int signalfd(int fd, const sigset_t *mask, int flags);
''')

class signalfd (object):
    '''signalfd(signal_set, [flags]) -> signalfd object

    Create a signalfd object for receiving the set of signals specified as
    a sigset object.
    '''

    def __init__ (self, signals, flags=None):
        if flags is None:
            self.flags = SFD_NONBLOCK
        else:
            self.flags = flags

        self.signals = signals
        self.fd = crt.signalfd(-1, self.signals.sigset, self.flags)

    def __enter__(self):
        self.oldsignals = sigprocmask(self.signals, SIG_BLOCK)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sigprocmask(self.oldsignals)
        self.close()
        return False

    def fileno(self):
        '''Return the integer file descriptor returned by signalfd(2).'''
        return self.fd

    def close(self):
        '''Close the signalfd object.  It cannot be used after this
        call.'''

        os.close(self.fd)

    def info(self):
        '''Return the next signalfd_siginfo structure available from the
        signalfd file descriptor.  The signalfd_siginfo structure has the
        following attributes:
        
        - ssi_signo -- Signal number
        - ssi_errno -- Error number (unused)
        - ssi_code -- Signal code
        - ssi_pid -- PID of sender
        - ssi_uid -- Real UID of sender
        - ssi_fd -- File descriptor (SIGIO)
        - ssi_tid -- Kernel timer ID (POSIX timers)
        - ssi_band -- Band event (SIGIO)
        - ssi_overrun -- POSIX timer overrun count
        - ssi_trapno -- Trap number that caused signal
        - ssi_status -- Exit status or signal (SIGCHLD)
        - ssi_int -- Integer sent by sigqueue(3)
        - ssi_ptr -- Pointer sent by sigqueue(3)
        - ssi_utime -- User CPU time consumed (SIGCHLD)
        - ssi_stime -- System CPU time consumed (SIGCHLD)
        - ssi_addr -- Address that generated signal (for hardware-generated signals)

        For example::

            info = sigfd.info()
            print 'Received signal: %d' % info.ssi_signo
        '''
        info = ffi.new('struct signalfd_siginfo *')
        buffer = ffi.buffer(info)
        buffer[:] = os.read(self.fd, ffi.sizeof('struct signalfd_siginfo'))
        return info

