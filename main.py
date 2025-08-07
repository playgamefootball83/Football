from pyrogram import idle
from bot import bot
from handlers import (
    start_football,
    join_team,
    assign_roles,
    start_match,
    play_rounds,
    end_game
)

# Register all handlers
start_football.register_handlers(bot)
join_team.register_handlers(bot)
assign_roles.register_handlers(bot)
start_match.register_handlers(bot)
play_rounds.register_handlers(bot)
end_game.register_handlers(bot)

print("⚽ Football bot is running...")
idle()
