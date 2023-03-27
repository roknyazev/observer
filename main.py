from observer import *

scan = scanner('./test', 5)
print(scan())
print(diff(scan(), scan()))
print(diff(None, scan()))

