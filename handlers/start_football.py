from pyrogram import filters
from pyrogram.types import Message
from bot import bot
from games.state_manager import create_game, is_game_running
from filters.custom_filters import is_referee

def register_handlers(bot):
    @bot.on_message(filters.command("start_football") & filters.group & is_referee)
    async def start_football(_, message: Message):
        chat_id = message.chat.id

        if is_game_running(chat_id):
            await message.reply("⚠️ Ek match already chal raha hai is group me.")
            return

        create_game(chat_id, message.from_user.id)
        await message.reply(
            "🏁 Football match started!\n\n"
            "Players can now join using:\n`/join_team A` or `/join_team B`\n\n"
            "Max: 8 teams, 8 players per team\n\n"
            "Referee: Only you can control this game."
        )
