import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatAction
from games.state_manager import get_game, update_game
from utils.commentary import get_commentary_text
from utils.mentions import mention_user


ACTION_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("⚽ KICK", callback_data="action_kick")],
    [InlineKeyboardButton("📤 PASS", callback_data="action_pass")],
    [InlineKeyboardButton("🛡 DEFENSIVE", callback_data="action_defensive")]
])


async def start_round(bot, chat_id, round_number):
    game = get_game(chat_id)
    if not game:
        return

    game["current_round"] = round_number
    game["round_actions"] = {}
    update_game(chat_id, game)

    team_a = game["current_match"]["team_a"]
    team_b = game["current_match"]["team_b"]

    players = game["teams"][team_a] + game["teams"][team_b]

    # DM buttons to players
    for user_id in players:
        try:
            await bot.send_chat_action(user_id, ChatAction.TYPING)
            await bot.send_message(
                user_id,
                f"🎮 Round {round_number} Started!\n\nChoose your move:",
                reply_markup=ACTION_BUTTONS
            )
        except Exception:
            pass  # User has blocked bot or not started

    await bot.send_message(
        chat_id,
        f"🎯 Round {round_number} started between 🅰️ {team_a} and 🅱️ {team_b}!\n"
        f"Players have 15 seconds to choose their actions!"
    )

    # Wait 15 seconds
    await asyncio.sleep(15)

    # Collect actions and apply AFK logic
    afk_users = []
    actions = game["round_actions"]

    for user_id in players:
        if str(user_id) not in actions:
            # Count AFK
            afk_count = game["afk_count"].get(str(user_id), 0) + 1
            game["afk_count"][str(user_id)] = afk_count

            if afk_count == 1:
                await bot.send_message(chat_id, f"⚠️ {mention_user(user_id)} did not respond (Yellow Card 🟨)")
            elif afk_count >= 2:
                await bot.send_message(chat_id, f"🚫 {mention_user(user_id)} removed for being AFK twice (Red Card 🟥)")
                # Remove from team
                for team in game["teams"]:
                    if user_id in game["teams"][team]:
                        game["teams"][team].remove(user_id)
        else:
            afk_users.append(user_id)

    update_game(chat_id, game)

    # Commentary
    action_list = game["round_actions"]
    commentary = get_commentary_text(action_list)
    await bot.send_message(chat_id, f"📢 **Round {round_number} Commentary:**\n{commentary}")
