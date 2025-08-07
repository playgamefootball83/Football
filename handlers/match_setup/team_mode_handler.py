from pyrogram.types import CallbackQuery
from bot import bot
from games.state_manager import create_game
from pyrogram import filters


@bot.on_callback_query(filters.regex(r"^select_mode:team$"))
async def handle_team_mode_select(bot, query: CallbackQuery):
    chat_id = query.message.chat.id
    user_id = query.from_user.id

    await query.answer()

    # Create new game instance
    create_game(chat_id, {
        "mode": "team",
        "referee": user_id,
        "teams": {"A": [], "B": []},
        "joined_users": {},
        "status": "waiting",
        "current_round": 0,
    })

    await query.message.edit_text(
        f"⚽ Team Match selected by referee: [{query.from_user.first_name}](tg://user?id={user_id})\n\n"
        "👥 Players can now join:\n"
        "- Use /join A or /join B\n\n"
        "Once teams are ready, referee can start match with /kickoff"
    )
