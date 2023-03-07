import asyncio
import os
import discord
from uuid import uuid4


async def play_audio_bytes(
    voice_client: discord.VoiceClient, audio_bytes: bytes
) -> None:
    file_name = str(uuid4()) + ".wav"
    with open(file_name, "wb") as temp_file:
        temp_file.write(audio_bytes)
    if voice_client and voice_client.is_connected():
        audio_source = discord.FFmpegPCMAudio(file_name)
        voice_client.play(audio_source, after=lambda e: print(f"Finished playing: {e}"))
    while voice_client.is_playing():
        await asyncio.sleep(0.1)
    os.remove(file_name)
