import ctypes
import os

# Load the compiled library
if os.name == "nt":  # Windows
    lib = ctypes.CDLL("./mycpp.dll")
else:  # Linux/Mac
    lib = ctypes.CDLL("./mycpp.so")

# Declare the argument and return types
lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
lib.add.restype = ctypes.c_int

# Call the function
result = lib.add(5, 7)
print("Result of add:", result)

# Call say_hello
lib.say_hello()
