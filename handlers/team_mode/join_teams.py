from pyrogram import filters
from pyrogram.types import Message, CallbackQuery
from bot import bot
from games.state_manager import get_game, update_game
from pyrogram.enums import ChatMemberStatus


def register_handlers(bot):
    # JOIN COMMAND HANDLERS
    @bot.on_message(filters.command(["join_team_a", "join_team_b"]) & filters.group)
    async def join_team_cmd(_, message: Message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        name = message.from_user.first_name
        command = message.command[0]

        team = "A" if command.endswith("a") else "B"
        await handle_join(chat_id, user_id, name, team, message)

    # JOIN BUTTON HANDLERS
    @bot.on_callback_query(filters.regex("^join_team_"))
    async def join_team_button(_, callback_query: CallbackQuery):
        chat_id = callback_query.message.chat.id
        user_id = callback_query.from_user.id
        name = callback_query.from_user.first_name
        team = callback_query.data.split("_")[-1]  # "A" or "B"

        await handle_join(chat_id, user_id, name, team, callback_query)


async def handle_join(chat_id, user_id, name, team, source):
    game = get_game(chat_id)

    if not game or not game.get("active") or game.get("mode") != "team_mode":
        await source.reply("❌ Koi active team match nahi hai.")
        return

    if user_id == game.get("referee"):
        await source.reply("🧑‍⚖️ Referee khud team me join nahi kar sakta.")
        return

    if user_id in game["teams"]["A"] or user_id in game["teams"]["B"]:
        await source.reply("⚠️ Tum pehle hi team me ho.")
        return

    if len(game["teams"][team]) >= 8:
        await source.reply(f"❌ Team {team} full ho chuki hai (8 players).")
        return

    # Add player
    game["teams"][team].append(user_id)
    update_game(chat_id, game)

    mention = f"[{name}](tg://user?id={user_id})"
    await source.reply(f"✅ {mention} joined Team {team}!")

    # Optional: edit message buttons to show updated counts (later)
