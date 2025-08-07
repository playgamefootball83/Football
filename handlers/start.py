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
            if not any(game["roles"].get(uid) == "captain" for uid in members):
                missing_roles.append(f"❌ Team {team_id} captain missing")
            if not any(game["roles"].get(uid) == "goalkeeper" for uid in members):
                missing_roles.append(f"❌ Team {team_id} goalkeeper missing")

        if missing_roles:
            await message.reply("⚠️ Can't start match:\n" + "\n".join(missing_roles))
            return

        game["round"] = 1
        await message.reply("✅ Match started!\n🎮 Round 1 will begin now.")
