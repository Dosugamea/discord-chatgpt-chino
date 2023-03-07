from io import BytesIO
import discord


def play_audio_bytes(voice_client: discord.VoiceClient, audio_bytes: bytes) -> None:
    audio_bytes = BytesIO(audio_bytes)

    if voice_client and voice_client.is_connected():
        audio_source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(audio_bytes), volume=0.5
        )
        voice_client.play(audio_source, after=lambda e: print(f"Finished playing: {e}"))
