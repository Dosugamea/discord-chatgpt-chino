import discord
from discord import Member, VoiceState
from discord.ext import commands
from external.chat_gpt import get_chatgpt_response
from external.vv import get_speaking_wave
from config import (
    DISCORD_BOT_TOKEN,
    ERROR_JOIN_VC_FIRST,
    ERROR_LONG_TEXT,
    ERROR_NOT_IN_VC,
    VV_SPEAKER_ID,
)
from util.validation import (
    clean_text,
    is_valid_text_message,
)
from util.voice import play_audio_bytes


intents = discord.Intents.default()
intents.message_content = True

voice_client: discord.VoiceClient | None = None
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command()
async def chat(ctx: commands.Context) -> None:
    global voice_client
    prompt = ctx.message.content
    if not is_valid_text_message(ctx.message):
        await ctx.send(ERROR_LONG_TEXT)
        return
    async with ctx.typing():
        result_text = get_chatgpt_response(prompt)
        result_text = clean_text(result_text)
        await ctx.send(result_text)
        if voice_client and voice_client.is_connected():
            audio_bytes = await get_speaking_wave(VV_SPEAKER_ID, result_text)
            await play_audio_bytes(voice_client, audio_bytes)


@bot.command()
async def join(ctx: commands.Context) -> None:
    global voice_client
    if not ctx.author.voice:
        await ctx.send(ERROR_JOIN_VC_FIRST)
        return
    channel = ctx.author.voice.channel
    voice_client = await channel.connect()


@bot.command()
async def leave(ctx: commands.Context) -> None:
    global voice_client
    if not voice_client or (not voice_client.is_connected()):
        await ctx.send(ERROR_NOT_IN_VC)
        return
    await voice_client.disconnect()


@bot.event
async def on_voice_state_update(
    member: Member, before: VoiceState, after: VoiceState
) -> None:
    global voice_client
    if (
        voice_client
        and voice_client.is_connected()
        and len(voice_client.channel.members) == 1
    ):
        await voice_client.disconnect()
        voice_client = None


@bot.event
async def on_ready() -> None:
    print("Logged in as {0.user}".format(bot))


if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
