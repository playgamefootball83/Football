from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot import bot
from filters.custom_filters import is_referee
from games.state_manager import get_game
from games.card_system import give_yellow_card
from games.action_engine import save_action
from utils.helpers import mention_user

import asyncio

ROUND_TIMEOUT = 20  # seconds

def register_handlers(bot):
    @bot.on_message(filters.command("start_round") & filters.group & is_referee)
    async def start_round(_, message: Message):
        chat_id = message.chat.id
        game = get_game(chat_id)

        if not game or not game["active"]:
            await message.reply("❌ Koi active match nahi hai.")
            return

        round_number = game["round"]
        await message.reply(f"🎮 Round {round_number} started!\nSending DM to players...")

        # Reset actions for this round
        game["actions"][round_number] = {}

        # Collect all players
        all_players = []
        for members in game["teams"].values():
            all_players.extend(members)

        # Send DM to all players
        for uid in all_players:
            try:
                await bot.send_message(
                    uid,
                    f"🎯 Round {round_number} – Choose your move!",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("⚽ KICK", callback_data=f"action_KICK_{chat_id}")],
                        [InlineKeyboardButton("🔁 PASS", callback_data=f"action_PASS_{chat_id}")],
                        [InlineKeyboardButton("🛡️ DEFENSIVE", callback_data=f"action_DEFENSIVE_{chat_id}")]
                    ])
                )
            except:
                pass  # Ignore blocked DMs

        # Wait for timeout
        await asyncio.sleep(ROUND_TIMEOUT)

        # Check who didn’t respond
        responded = game["actions"][round_number].keys()
        for uid in all_players:
            if uid not in responded:
                give_yellow_card(chat_id, uid)

        await message.reply("✅ Round finished! Players who didn’t respond received ⚠️ Yellow cards.")
        game["round"] += 1


    @bot.on_callback_query(filters.regex(r"action_(KICK|PASS|DEFENSIVE)_(\d+)"))
    async def handle_action(_, query: CallbackQuery):
        action = query.matches[0].group(1)
        chat_id = int(query.matches[0].group(2))
        user_id = query.from_user.id

        game = get_game(chat_id)
        if not game or not game["active"]:
            await query.answer("⛔ Match khatam ho gaya hai.", show_alert=True)
            return

        round_number = game["round"]

        if user_id in game["actions"][round_number]:
            await query.answer("❌ Tumne already move select kiya.", show_alert=True)
            return

        save_action(chat_id, round_number, user_id, action)
        await query.answer(f"✅ You chose {action}", show_alert=True)
