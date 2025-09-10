import ctypes
import os

# Load compiled C++ shared library
lib_path = os.path.abspath("./video_editor.so")  # Linux/Mac
# For Windows use: lib_path = os.path.abspath("./video_editor.dll")

video_lib = ctypes.CDLL(lib_path)

# Define argument types
video_lib.edit_video.argtypes = [
    ctypes.c_char_p,  # main video path
    ctypes.c_char_p,  # sponsor video path
    ctypes.c_char_p,  # output video path
    ctypes.c_double   # cut time in seconds
]
video_lib.edit_video.restype = ctypes.c_int  # return type

# Paths
main_video = b"main_video.mp4"
sponsor_video = b"sponsor_video.mp4"
output_video = b"final_output.mp4"

# Call the C++ function
result = video_lib.edit_video(main_video, sponsor_video, output_video, 5.0)

if result == 0:
    print("Video edited successfully! Output:", output_video.decode())
else:
    print("Video editing failed.")
