from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import bot
from games.state_manager import create_game, get_game
from filters.admins_only import admins_only


def register_handlers(bot):
    @bot.on_message(filters.command("start_team_match") & filters.group & admins_only)
    async def start_team_match(_, message: Message):
        chat_id = message.chat.id
        user_id = message.from_user.id

        existing_game = get_game(chat_id)
        if existing_game and existing_game.get("active"):
            await message.reply("❌ Ek match already chal raha hai. Pehle usse khatam karo.")
            return

        # Create base game state
        create_game(chat_id, {
            "mode": "team_mode",
            "referee": user_id,
            "teams": {
                "A": [],
                "B": []
            },
            "roles": {
                "A": {"captain": None, "goalkeeper": None},
                "B": {"captain": None, "goalkeeper": None}
            },
            "round": 1,
            "actions": {},
            "cards": {},
            "active": True
        })

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔵 Join Team A", callback_data="join_team_A"),
                InlineKeyboardButton("🔴 Join Team B", callback_data="join_team_B")
            ]
        ])

        await message.reply(
            "🏁 **Team Match Started!**\n\n"
            "Players can now join by clicking the buttons below.\n"
            "🔒 Only game admins can start the match.\n"
            f"🧑‍⚖️ Referee: {message.from_user.mention}",
            reply_markup=buttons
        )
