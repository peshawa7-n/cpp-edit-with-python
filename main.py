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

api_id = os.getenv("APITELEGRAM_ID")
api_hash = os.getenv("APITELEGRAM_HASH")
channel_to_send = -1002956642937

DOWNLOADS_DIR = "downloads100"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)
client = TelegramClient("superman.session", api_id, api_hash)
client.start()


def create_path(path_str):
    """
    Create each directory in the given path one by one if it doesn't exist.
    Example: sponsor/taste/i
    """
    parts = path_str.split(os.sep)  # split by folder separator (/ or \)
    current_path = ""

    for part in parts:
        if not part:  # skip empty parts (e.g., if path starts with /)
            continue
        current_path = os.path.join(current_path, part)
        if not os.path.exists(current_path):
            os.mkdir(current_path)
            print(f"Created: {current_path}")
        else:
            print(f"Exists: {current_path}")


def get_available_filename(base_name, ext=".mp4"):
    i = 1
    filename = f"{base_name}{ext}"
    while os.path.exists(filename):
        filename = f"{base_name}_{i}{ext}"
        i += 1
    return filename


def download_and_forward(chat, limit):
    # isdownload = True
    messages = client.get_messages(chat, limit=limit)

    reverse_data = messages[::-1]

    # all_listed_id = [message.id for message in messages if "چیرۆکی شەوێک" in message.text and message.media]

    # max_id = max(all_listed_id) if all_listed_id else print("No messages found with the specified text and media.")


    for msg in tqdm.tqdm(reverse_data):


        # if msg.media and "چیرۆکی شەوێک" in msg.text:
        if msg.media:


            # for message2 in tqdm.tqdm(messages) if message2.media and "چیرۆکی شەوێک" in message2.text and message2.id == max_id:
            #     current_max_id = msg.id
            #     DOWNLOAD_VIDEO = message2

            

            try:
                
                print(f"\n📥 Downloading media from message ID {msg.id} {msg.text}...")
                filename = client.download_media(msg, DOWNLOADS_DIR)

                if filename:

                    # edited_path = edit_video(filename)
                    print(f"\n✅ Downloaded: {filename}")

                    # Send to another channel
                    client.send_file(channel_to_send, filename, caption=f"{msg.text}", supports_streaming=True)
                    print(f"🚀 Sent to {channel_to_send}\n")

                    # Delete file
                    os.remove(filename)
                    print(f"🗑️ Deleted {filename}")

            except Exception as e:
                print(f"❌ file Error : {e}")

limit = 200
source = "hadia_gull"
download_and_forward(source, limit)
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
