from pyrogram import filters
from pyrogram.types import Message
from bot import bot
from filters.custom_filters import is_referee
from games.state_manager import get_game, end_game
from utils.helpers import mention_user

def register_handlers(bot):
    @bot.on_message(filters.command("end_match") & filters.group & is_referee)
    async def end_match(_, message: Message):
        chat_id = message.chat.id
        game = get_game(chat_id)

        if not game or not game["active"]:
            await message.reply("❌ Koi active match nahi hai.")
            return

        round_number = game["round"] - 1  # last completed
        final_actions = game["actions"].get(round_number, {})
        yellow_red = game.get("cards", {})

        action_summary = ""
        for uid, act in final_actions.items():
            action_summary += f"• {mention_user(uid)} → `{act}`\n"

        card_summary = ""
        for uid, cards in yellow_red.items():
            y = cards.get("yellow", 0)
            r = cards.get("red", 0)
            if y or r:
                card_summary += f"{mention_user(uid)} - {y} ⚠️ | {r} 🔴\n"

        reply_text = "🏁 **Match Ended!**\n\n"
        if action_summary:
            reply_text += "🎯 **Last Round Actions:**\n" + action_summary + "\n"
        if card_summary:
            reply_text += "📛 **Cards Issued:**\n" + card_summary

        await message.reply(reply_text or "Match ended, no summary available.")
        end_game(chat_id)
