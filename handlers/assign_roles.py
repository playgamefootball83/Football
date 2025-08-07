from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from bot import bot
from games.state_manager import get_game
from filters.custom_filters import is_referee
from utils.helpers import mention_user

def register_handlers(bot):
    @bot.on_message(filters.command("assign_roles") & filters.group & is_referee)
    async def assign_roles(_, message: Message):
        chat_id = message.chat.id
        game = get_game(chat_id)

        if not game or not game["active"]:
            await message.reply("❌ Koi active tournament nahi hai.")
            return

        keyboard = []
        for team_id in sorted(game["teams"].keys(), key=int):
            keyboard.append([
                InlineKeyboardButton(
                    text=f"⚽ Select Team {team_id}",
                    callback_data=f"select_team_{team_id}"
                )
            ])

        await message.reply(
            "👇 Select team to assign Captain/Goalkeeper:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    @bot.on_callback_query(filters.regex(r"select_team_(\d+)"))
    async def team_selected(_, query: CallbackQuery):
        chat_id = query.message.chat.id
        team_id = query.data.split("_")[-1]
        game = get_game(chat_id)

        players = game["teams"].get(team_id, [])
        if not players:
            await query.answer("⚠️ Team empty hai", show_alert=True)
            return

        keyboard = []
        for uid in players:
            keyboard.append([
                InlineKeyboardButton(
                    text=f"🎖️ Captain",
                    callback_data=f"set_role_{team_id}_captain_{uid}"
                ),
                InlineKeyboardButton(
                    text=f"🧤 Goalkeeper",
                    callback_data=f"set_role_{team_id}_goalkeeper_{uid}"
                )
            ])

        await query.message.reply(
            f"👥 Players in Team {team_id}: Select role",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    @bot.on_callback_query(filters.regex(r"set_role_(\d+)_(captain|goalkeeper)_(\d+)"))
    async def set_role(_, query: CallbackQuery):
        chat_id = query.message.chat.id
        team_id, role, user_id = query.matches[0].groups()
        user_id = int(user_id)
        game = get_game(chat_id)

        if not game:
            return

        # Prevent multiple roles per team
        for uid, r in game["roles"].items():
            if r == role and uid in game["teams"].get(team_id, []):
                await query.answer(f"⚠️ Team {team_id} already has a {role}.", show_alert=True)
                return

        game["roles"][user_id] = role
        await query.message.reply(f"{mention_user(user_id)} has been assigned as **{role.upper()}** of Team {team_id} ✅")
