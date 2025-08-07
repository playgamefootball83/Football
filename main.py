from pyrogram import idle
from bot import bot
from handlers import start, join_team, play_rounds

start.register_handlers(bot)
join_team.register_handlers(bot)
play_rounds.register_handlers(bot)

print("⚽ Football bot is running...")
idle()
