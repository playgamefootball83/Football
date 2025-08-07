from pyrogram import filters
from pyrogram.types import Message
from bot import bot
from games.state_manager import get_game, update_game
from handlers.team_mode.rounds import start_round


def register_handlers(bot):
    @bot.on_message(filters.command("next_round") & filters.group)
    async def next_round(_, message: Message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        game = get_game(chat_id)

        if not game or not game.get("active") or not game.get("started"):
            await message.reply("❌ Koi active match nahi chal raha.")
            return

        if user_id != game.get("referee"):
            await message.reply("🚫 Sirf referee hi next round chala sakta hai.")
            return

        current = game.get("current_round", 0)
        if current >= 3:
            await message.reply("✅ 3 rounds complete ho chuke hain. Match finished!")
            game["active"] = False
            update_game(chat_id, game)
            return

        await message.reply(f"🔁 Starting Round {current + 1}...")
        await start_round(bot, chat_id, current + 1)
