from pyrogram import filters
from pyrogram.types import Message
from bot import bot
from games.state_manager import get_game
from filters.custom_filters import is_game_group

MAX_TEAMS = 8
MAX_PLAYERS_PER_TEAM = 8

def register_handlers(bot):
    @bot.on_message(filters.command("join_team") & filters.group & is_game_group)
    async def join_team(_, message: Message):
        chat_id = message.chat.id
        user = message.from_user
        game = get_game(chat_id)

        if not game or not game["active"]:
            await message.reply("❌ Koi tournament active nahi hai.")
            return

        if user.id == game["referee"]:
            await message.reply("🚫 Referee khud team join nahi kar sakta.")
            return

        parts = message.text.split()
        if len(parts) < 2 or not parts[1].isdigit():
            await message.reply("⚠️ Usage: /join_team [1-8]")
            return

        team_id = int(parts[1])
        if team_id < 1 or team_id > MAX_TEAMS:
            await message.reply("⚠️ Sirf 1 se 8 tak ki team join kar sakte ho.")
            return

        team_key = str(team_id)
        teams = game["teams"]

        # Prevent joining multiple teams
        for tid, members in teams.items():
            if user.id in members:
                await message.reply(f"⚠️ {user.mention}, tum already Team {tid} me ho.")
                return

        # Add team if not exist
        if team_key not in teams:
            teams[team_key] = []

        if len(teams[team_key]) >= MAX_PLAYERS_PER_TEAM:
            await message.reply(f"🚫 Team {team_key} full ho chuki hai (max {MAX_PLAYERS_PER_TEAM}).")
            return

        teams[team_key].append(user.id)
        await message.reply(f"✅ {user.mention} joined Team {team_key} successfully.")
