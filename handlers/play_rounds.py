from pyrogram import filters
from pyrogram.types import Message
from bot import bot
from states.game_state import game_data
import random

def register_handlers(bot):
    @bot.on_message(filters.command("play_round") & filters.group)
    async def play_round(_, message: Message):
        chat_id = message.chat.id
        if chat_id not in game_data or not game_data[chat_id]["active"]:
            await message.reply("❌ No active game.")
            return

        game = game_data[chat_id]
        game["round"] += 1

        team_a_score = random.randint(0, 3)
        team_b_score = random.randint(0, 3)

        await message.reply(
            f"🎮 Round {game['round']} Result:\n\n"
            f"Team A: {team_a_score} goals\n"
            f"Team B: {team_b_score} goals"
        )

        if game["round"] >= 3:
            game["active"] = False
            await message.reply("🏁 Match ended!")
