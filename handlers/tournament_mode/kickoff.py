from pyrogram import filters
from pyrogram.types import Message
from bot import bot
from games.state_manager import get_game
from handlers.tournament_mode.rounds import start_round


@bot.on_message(filters.command("kickoff") & filters.group)
async def kickoff_tournament(bot, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    game = get_game(chat_id)
    if not game or game["mode"] != "tournament":
        return await message.reply("❌ No active tournament game in this group.")

    if user_id != game.get("referee"):
        return await message.reply("🚫 Only the referee can start the match.")

    match = game.get("current_match")
    if not match or "team_a" not in match or "team_b" not in match:
        return await message.reply("❌ No teams are currently selected to play.")

    team_a = match["team_a"]
    team_b = match["team_b"]

    await message.reply(
        f"🚩 Match starting between 🅰️ {team_a} and 🅱️ {team_b}!\n"
        f"⏳ Referee has started Round 1!"
    )

    await start_round(bot, chat_id, round_number=1)
