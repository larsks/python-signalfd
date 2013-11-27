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
        return False

    def fileno(self):
        return self.fd

    def close(self):
        os.close(self.fd)

    def info(self):
        info = ffi.new('struct signalfd_siginfo *')
        buffer = ffi.buffer(info)
        buffer[:] = os.read(self.fd, ffi.sizeof('struct signalfd_siginfo'))
        return info

