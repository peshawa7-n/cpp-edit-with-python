import ctypes
import os
from telethon import TelegramClient
from dotenv import load_dotenv
from tqdm import tqdm
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

# ------------------------------------------------------------------------------
# Load environment variables
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE_NUMBER")

# Directory to save downloads
DOWNLOAD_DIR = "downloads"

# Ensure download folder exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Create the Telegram client
client = TelegramClient("telegram_session", API_ID, API_HASH)

async def download_media_from_chat(chat_username, limit=10):
    """
    Downloads media from a given Telegram chat.
    """
    print(f"Connecting to Telegram...")
    await client.start()

    print(f"Fetching messages from {chat_username}...")

    # Loop through messages and download media
    async for message in client.iter_messages(chat_username, limit=limit):
        if message.media:  # Only download if message contains media
            file_path = await message.download_media(file=DOWNLOAD_DIR)
            print(f"Downloaded: {file_path}")

    print("Download completed!")

# Run the script
with client:
    client.loop.run_until_complete(download_media_from_chat("your_channel_or_group_username", limit=20))

# ------------------------------------------------------------------------------
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
