from pyrogram import filters
from pyrogram.types import Message
from bot import bot
from games.state_manager import get_game
from handlers.tournament_mode.rounds import start_round


@bot.on_message(filters.command("next_round") & filters.group)
async def next_round_tournament(bot, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    game = get_game(chat_id)
    if not game or game["mode"] != "tournament":
        return await message.reply("❌ No active tournament game in this group.")

    if user_id != game.get("referee"):
        return await message.reply("🚫 Only the referee can trigger the next round.")

    current_round = game.get("current_round", 0)
    if current_round >= 3:
        return await message.reply("✅ All 3 rounds have already been played!")

    next_round = current_round + 1

    await message.reply(f"🎯 Starting Round {next_round}...")
    await start_round(bot, chat_id, round_number=next_round)
