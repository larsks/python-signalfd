#!/usr/bin/python

import os
import sys

from .common import ffi, crt
from .constants import *

ffi.cdef('''
typedef struct {
    unsigned long int __val[%d];
  } sigset_t;
''' % (1024/(8 * ffi.sizeof('unsigned long int'))))

ffi.cdef('''
int sigemptyset(sigset_t *set);
int sigfillset(sigset_t *set);
int sigaddset(sigset_t *set, int signum);
int sigdelset(sigset_t *set, int signum);
int sigismember(const sigset_t *set, int signum);
int sigprocmask(int how, const sigset_t *set, sigset_t *oldset);
''')

class sigset (object):
    '''This is a thin wrapper over sigsetops(3)'''

    def __init__ (self, signals=None):
        self.sigset = ffi.new('sigset_t *')
        self.empty()

        if signals is not None:
            self.sigset = signals

    def empty(self):
        '''Initialize the signal set to empty'''
        crt.sigemptyset(self.sigset)

    def fill(self):
        '''Initialize the signal set to full, including all signals'''
        crt.sigfillset(self.sigset)

    def add(self, sig):
        '''Add the specified signal to the signal set'''
        crt.sigaddset(self.sigset, sig)

    def remove(self, sig):
        '''Remove the specified signal from the signal set'''
        crt.sigdelset(self.sigset, sig)

    def ismember(self, sig):
        '''Test if the specified signal is a member of the signal set'''
        return crt.sigismember(self.sigset, sig) == 1

def sigprocmask(signals, mode=SIG_SETMASK):
    '''Examine and change blocked signals

    - `signals` is a sigset object.
    - `mode` controls how sigprocmask() interprets the signal mask (see
      below)
    
    sigprocmask() is used to fetch and/or change the signal mask of the calling thread.
    The signal mask is the set of signals whose delivery is currently blocked  for  the
    caller (see also signal(7) for more details).
 
    The behavior of the call is dependent on the value of mode, as follows.
 
    signalfd.SIG_BLOCK
           The set of blocked signals is the union of the current set and the set
           argument.
 
    signalfd.SIG_UNBLOCK
           The signals in set are removed from the current set of blocked signals.   It
           is permissible to attempt to unblock a signal which is not blocked.
 
    signalfd.SIG_SETMASK
           The set of blocked signals is set to the argument set.

    '''

    if not mode in [SIG_BLOCK, SIG_UNBLOCK, SIG_SETMASK]:
        raise ValueError('invalid mode')

    oldsignals = ffi.new('sigset_t *')
    res = crt.sigprocmask(mode, signals.sigset, oldsignals)
    if res < 0:
        raise OSError()

    return sigset(oldsignals)

