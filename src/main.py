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
    has_mention,
    is_from_bot,
    is_self_message,
    is_valid_text_message,
)
from util.voice import play_audio_bytes


client = discord.Client()
voice_client: discord.VoiceClient | None = None
bot = commands.Bot(command_prefix="!")


@client.event
async def on_message(message: discord.Message) -> None:
    global voice_client

    if is_self_message(message, client.user.id):
        return
    if is_from_bot(message):
        return
    if has_mention(message):
        return

    if not is_valid_text_message(message):
        await message.channel.send(ERROR_LONG_TEXT)
        return

    text = message.content
    if text.startswith("!chat"):
        prompt = " ".join(text.split(" ")[1:])
        async with message.channel.typing():
            result_text = get_chatgpt_response(prompt)
            result_text = clean_text(result_text)
            await message.channel.send(result_text)
            if voice_client and voice_client.is_connected():
                audio_bytes = await get_speaking_wave(VV_SPEAKER_ID, result_text)
                await play_audio_bytes(voice_client, audio_bytes)
    elif text.startswith("!join"):
        if not message.author.voice:
            await message.channel.send(ERROR_JOIN_VC_FIRST)
            return
        channel = message.author.voice.channel
        voice_client = await channel.connect()
    elif text.startswith("!leave"):
        if not voice_client or not voice_client.is_connected():
            await message.channel.send(ERROR_NOT_IN_VC)
            return
        await voice_client.disconnect()
        voice_client = None


@bot.command(name="chat")
async def cmd_chat(ctx: commands.Context) -> None:
    global voice_client
    prompt = ctx.message
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
async def cmd_join(ctx: commands.Context) -> None:
    global voice_client
    if not ctx.author.voice:
        await ctx.send(ERROR_JOIN_VC_FIRST)
        return
    channel = ctx.author.voice.channel
    voice_client = await channel.connect()


@client.command()
async def cmd_leave(ctx: commands.Context) -> None:
    global voice_client
    if not voice_client or not voice_client.is_connected():
        await ctx.send(ERROR_NOT_IN_VC)
        return
    await voice_client.disconnect()


@client.event
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


@client.event
async def on_ready() -> None:
    print("Logged in as {0.user}".format(client))


if __name__ == "__main__":
    client.run(DISCORD_BOT_TOKEN)
