from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import bot
from games.state_manager import create_game, get_game

@bot.on_message(filters.command("start_football") & filters.group)
async def select_mode(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    existing_game = get_game(chat_id)
    if existing_game and existing_game.get("active"):
        await message.reply("❗ Ek match already active hai. Use `/end_game` se end karo.")
        return

    # Register new game state
    create_game(chat_id)
    game = get_game(chat_id)
    game["referee"] = user_id
    game["active"] = True
    game["mode"] = None
    game["started"] = False
    game["teams"] = {}
    game["afk_count"] = {}
    game["round_actions"] = {}
    game["current_round"] = 0

    await message.reply(
        f"⚽ **Football Game Started!**\n\n"
        f"👤 Referee: [Click here](tg://user?id={user_id})\n\n"
        "Choose the match type below to continue:",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🏆 Tournament Mode", callback_data="mode_tournament"),
                InlineKeyboardButton("🤝 Team-vs-Team Mode", callback_data="mode_team"),
            ]
        ])
    )
