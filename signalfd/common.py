#!/usr/bin/python

from cffi import FFI

ffi = FFI()
crt = ffi.dlopen(None)

ffi.cdef('''
typedef unsigned int uint32_t;
typedef int int32_t;
typedef unsigned long int uint64_t;
typedef unsigned char uint8_t;
''')

