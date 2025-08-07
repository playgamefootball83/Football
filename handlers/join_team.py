from pyrogram import filters
from pyrogram.types import Message
from bot import bot
from states.game_state import game_data

def register_handlers(bot):
    @bot.on_message(filters.command("join_team") & filters.group)
    async def join_team(_, message: Message):
        chat_id = message.chat.id
        if chat_id not in game_data or not game_data[chat_id]["active"]:
            await message.reply("❌ No game running.")
            return

        parts = message.text.split()
        if len(parts) < 2 or parts[1] not in ["A", "B"]:
            await message.reply("Usage: /join_team A or B")
            return

        team = parts[1]
        user_id = message.from_user.id
        user_mention = message.from_user.mention

        if user_id in game_data[chat_id]["teams"]["A"] or user_id in game_data[chat_id]["teams"]["B"]:
            await message.reply(f"{user_mention}, you already joined.")
            return

        game_data[chat_id]["teams"][team].append(user_id)
        await message.reply(f"{user_mention} joined Team {team} ✅")
