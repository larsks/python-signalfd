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
    '''Examine and change blocked signals'''

    print 'SIGS', [x for x in signals.sigset.__val]

    if not mode in [SIG_BLOCK, SIG_UNBLOCK, SIG_SETMASK]:
        raise ValueError('invalid mode')

    oldsignals = ffi.new('sigset_t *')
    res = crt.sigprocmask(mode, signals.sigset, oldsignals)
    if res < 0:
        raise OSError()

    return sigset(oldsignals)

