from ctypes import *

from cffi.backend_ctypes import xrange

print(cdll.msvcrt)# Prints `<CDLL 'msvcrt', handle ... at ...>`
libc = cdll.msvcrt
libc.printf("%d\n", 42)
text = c_char_p("Hello, World")
count = c_long(333)
for i in xrange(0, count):
    libc.puts(text)
