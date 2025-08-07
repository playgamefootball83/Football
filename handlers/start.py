from pyrogram import filters
from pyrogram.types import Message
from bot import bot
from states.game_state import game_data

def register_handlers(bot):
    @bot.on_message(filters.command("start_football") & filters.group)
    async def start_football(_, message: Message):
        chat_id = message.chat.id
        if chat_id in game_data:
            await message.reply("⚠️ Game already running.")
            return
        game_data[chat_id] = {
            "teams": {"A": [], "B": []},
            "round": 0,
            "active": True
        }
        await message.reply("🏁 Football game started!\n\nPlayers use /join_team A or B to join.")
