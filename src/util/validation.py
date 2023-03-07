import re
import discord


def has_mention(message: discord.Message) -> bool:
    return len(message.mentions) > 0


def is_valid_text_message(message: discord.Message) -> bool:
    text = message.content.strip()
    max_message_length = 2048
    return len(text) <= max_message_length


def is_self_message(message: discord.Message, bot_user_id: str) -> bool:
    return message.author == bot_user_id


def is_from_bot(message: discord.Message) -> bool:
    return message.author.bot is True


def is_mentioned(message: discord.Message, bot_user_id: str) -> bool:
    mentioned_users = message.mentions
    bot_mentioned = any(user.id == bot_user_id for user in mentioned_users)
    has_mention_in_text = f"<@!{bot_user_id}>" in message.content
    return has_mention_in_text and bot_mentioned


def clean_text(content: str) -> str:
    """読み上げるテキストを整形する"""
    # 絵文字除去
    content = re.sub(r"<a?:([a-zA-Z_]+):\d+>", r"\1", content)
    # URL除去(置き換え)
    content = re.sub(r"https?://[^\s]+", r"URL", content)
    # コード除去
    content = re.sub(r"```[\s\S]*```", r"コード", content)
    return re.sub(r"[\n\r]", "", content)
