from pyrogram import filters
from pyrogram.types import Message
from bot import bot
from games.state_manager import get_game, update_game


def register_handlers(bot):
    @bot.on_message(filters.command("kickoff") & filters.group)
    async def kickoff(_, message: Message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        game = get_game(chat_id)

        if not game or not game.get("active") or game.get("mode") != "team_mode":
            await message.reply("❌ Koi active team match nahi hai.")
            return

        if user_id != game.get("referee"):
            await message.reply("🚫 Sirf referee hi kickoff kar sakta hai.")
            return

        if game.get("started"):
            await message.reply("⚠️ Match already shuru ho chuka hai.")
            return

        # Check players
        if len(game["teams"]["A"]) < 1 or len(game["teams"]["B"]) < 1:
            await message.reply("❌ Har team me kam se kam 1 player hona chahiye.")
            return

        # Check roles
        for team in ["A", "B"]:
            if not game["roles"][team]["captain"] or not game["roles"][team]["goalkeeper"]:
                await message.reply(f"⚠️ Team {team} ka captain ya goalkeeper assign nahi hua.")
                return

        # Mark match started
        game["started"] = True
        update_game(chat_id, game)

        await message.reply(
            "🚀 **Kickoff!** Match officially started between Team A and Team B.\n"
            "Get ready for Round 1!"
        )

        # 🧠 Start Round 1 Logic
        from handlers.team_mode.rounds import start_round
        await start_round(bot, chat_id, 1)
