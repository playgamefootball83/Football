import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from bot import bot
from games.state_manager import get_game, update_game, active_games
from pyrogram import filters


# Actions to be collected per round
ACTIONS = ["KICK", "PASS", "DEFENSIVE"]


async def start_round(bot, chat_id, round_number):
    game = get_game(chat_id)
    if not game or not game.get("active"):
        return

    game["current_round"] = round_number
    game["round_actions"] = {}
    update_game(chat_id, game)

    players = game["teams"]["A"] + game["teams"]["B"]

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚽ KICK", callback_data=f"action_KICK")],
        [InlineKeyboardButton("🔁 PASS", callback_data=f"action_PASS")],
        [InlineKeyboardButton("🛡 DEFENSIVE", callback_data=f"action_DEFENSIVE")]
    ])

    # DM players
    for player_id in players:
        try:
            await bot.send_message(
                player_id,
                f"🎮 **Round {round_number} Started!**\nChoose your action:",
                reply_markup=keyboard
            )
        except:
            pass  # can't DM user

    # Wait 15 seconds
    await asyncio.sleep(15)

    # Evaluate round
    game = get_game(chat_id)
    actions = game.get("round_actions", {})
    commentary = f"📢 **Round {round_number} Results:**\n\n"

    for player_id in players:
        name = f"[Player](tg://user?id={player_id})"
        if player_id in actions:
            commentary += f"✅ {name} chose **{actions[player_id]}**\n"
        else:
            # AFK
            game["afk_count"][str(player_id)] = game["afk_count"].get(str(player_id), 0) + 1
            if game["afk_count"][str(player_id)] == 1:
                commentary += f"🟡 {name} was AFK (Yellow Card)\n"
            elif game["afk_count"][str(player_id)] >= 2:
                # Remove from team
                for team in ["A", "B"]:
                    if player_id in game["teams"][team]:
                        game["teams"][team].remove(player_id)
                commentary += f"🔴 {name} was AFK again and got a Red Card!\n"

    update_game(chat_id, game)

    await bot.send_message(chat_id, commentary)


# Handle player actions
@bot.on_callback_query(filters.regex("^action_"))
async def handle_player_action(_, callback: CallbackQuery):
    user_id = callback.from_user.id
    action = callback.data.split("_")[-1]

    # Find which game user is in
    for chat_id, game in active_games.items():
        if user_id in game["teams"]["A"] or user_id in game["teams"]["B"]:
            if game.get("started") and not game.get("mode") != "team_mode":
                game["round_actions"][user_id] = action
                update_game(chat_id, game)
                await callback.answer(f"✅ Action selected: {action}", show_alert=True)
                return

    await callback.answer("❌ No active round found or you're not in the match.", show_alert=True)
