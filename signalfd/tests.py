#!/usr/bin/python

import select
import signal
from .sigset import sigset, sigprocmask
from .signalfd import signalfd

def test_sigset_create():
    '''Test that we can create a sigset object'''
    assert sigset() is not None

def test_sigset_membership():
    '''Test that add/delete/addmember behave sanely'''

    signals = sigset()
    signals.add(signal.SIGHUP)
    signals.add(signal.SIGINT)

    assert signals.ismember(signal.SIGHUP)
    assert signals.ismember(signal.SIGINT)

    signals.remove(signal.SIGINT)

    assert not signals.ismember(signal.SIGINT)

def test_signalfd_create():
    '''Test that we can create a signalfd object'''
    signals = sigset()
    assert signalfd(signals) is not None

def test_sigmask_restore():
    '''Test that signal mask has been restored after signalfd context
    manager exits'''

    empty = sigset()
    orig = sigprocmask(empty)

    mask = sigset()
    mask.add(signal.SIGHUP)
    mask.add(signal.SIGINT)

    with signalfd(mask) as fd:
        pass

    final = sigprocmask(empty)

    assert all([x == final.sigset.__val[i]
        for i,x in enumerate(orig.sigset.__val)])

def test_alarm():
    '''Test that we can read a signal from a signalfd'''

    mask = sigset()
    mask.add(signal.SIGALRM)

    with signalfd(mask) as fd:
        poll = select.poll()
        poll.register(fd,  select.POLLIN)

        signal.alarm(1)
        events = dict(poll.poll(2000))
        assert fd.fileno() in events
        assert fd.info().ssi_signo == signal.SIGALRM

