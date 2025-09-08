import ctypes

# Load the shared library
mylib = ctypes.CDLL("./mylib.so")  # or "mylib.dll" on Windows

# Call function
result = mylib.add(5, 7)
print("Result:", result)

