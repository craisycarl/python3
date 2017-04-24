import sys

print(sys.version)
print(sys.version[0])

if sys.version_info[0] == 3:
    from importlib import abc
else:
    from importlib2 import abc

