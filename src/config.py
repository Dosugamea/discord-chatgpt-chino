import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHATGPT_API_KEY = os.getenv("CHATGPT_API_KEY")
ERROR_LONG_TEXT = (
    "Sorry, the prompt is too long. Please try again with a shorter prompt."
)
ERROR_JOIN_VC_FIRST = "You need to be in a voice channel to use this command."
ERROR_NOT_IN_VC = "I am not connected to a voice channel."

VV_ENDPOINT_QUERY = os.getenv("VV_ENDPOINT_QUERY")
VV_ENDPOINT_SPEAKER = os.getenv("VV_ENDPOINT_SPEAKER")
VV_ENDPOINT_AUDIO = os.getenv("VV_ENDPOINT_AUDIO")
VV_SPEAKER_ID = os.getenv("VV_SPEAKER_ID")
