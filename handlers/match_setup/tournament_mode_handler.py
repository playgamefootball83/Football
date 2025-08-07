from pyrogram.types import CallbackQuery
from bot import bot
from games.state_manager import create_game
from pyrogram import filters
from pyrogram.types import Message

@bot.on_callback_query(filters.regex(r"^select_mode:tournament$"))
async def handle_tournament_mode_select(bot, query: CallbackQuery):
    chat_id = query.message.chat.id
    user_id = query.from_user.id

    await query.answer()  # remove loading circle

    # Create a new game
    create_game(chat_id, {
        "mode": "tournament",
        "referee": user_id,
        "teams": {},
        "joined_users": {},
        "status": "waiting",
        "current_match": {},
        "current_round": 0,
        "match_history": [],
        "eliminated": []
    })

    await query.message.edit_text(
        f"🏆 Tournament mode selected by referee: [{query.from_user.first_name}](tg://user?id={user_id})\n\n"
        "📝 Now send the command /create_team <team_name> to create teams (up to 8).\n"
        "👥 Players can join a team using /join <team_name>.\n\n"
        "Once teams are full, use /begin_match to start the tournament!"
    )
