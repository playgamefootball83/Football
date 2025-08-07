from pyrogram import filters
from pyrogram.types import Message
from bot import bot
from filters.custom_filters import is_referee
from games.state_manager import get_game
from utils.helpers import mention_user

def register_handlers(bot):
    @bot.on_message(filters.command("start_match") & filters.group & is_referee)
    async def start_match(_, message: Message):
        chat_id = message.chat.id
        game = get_game(chat_id)

        if not game or not game["active"]:
            await message.reply("❌ Koi active tournament nahi hai.")
            return

        missing_roles = []

        for team_id, members in game["teams"].items():
            team_captain = None
            team_goalkeeper = None

            for uid in members:
                if game["roles"].get(uid) == "captain":
                    team_captain = uid
                if game["roles"].get(uid) == "goalkeeper":
                    team_goalkeeper = uid

            if not team_captain:
                missing_roles.append(f"❌ Team {team_id} ka **captain** missing hai.")
            if not team_goalkeeper:
                missing_roles.append(f"❌ Team {team_id} ka **goalkeeper** missing hai.")

        if missing_roles:
            await message.reply("⚠️ Match start nahi ho sakta:\n\n" + "\n".join(missing_roles))
            return

        # All roles assigned, start match
        game["round"] = 1
        await message.reply("✅ All teams are ready!\n\n🏟 Match is starting...\n\n🎮 Round 1 will begin shortly.")
