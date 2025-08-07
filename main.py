from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from pyrogram.handlers import MessageHandler

# Bot initialize
bot = Client("football_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Import handlers for tournament and team modes
import handlers.match_setup.start
import handlers.match_setup.join
import handlers.match_setup.roles
import handlers.match_setup.kickoff

# TEAM MODE imports (rename matched)
import handlers.team_mode.start_team_match
import handlers.team_mode.join_teams
import handlers.team_mode.assign_roles
import handlers.team_mode.kickoff_team_match
import handlers.team_mode.rounds
import handlers.team_mode.next_round

# TOURNAMENT MODE imports
import handlers.tournament_mode.start_tournament
import handlers.tournament_mode.join_teams
import handlers.tournament_mode.assign_roles
import handlers.tournament_mode.kickoff_tournament
import handlers.tournament_mode.rounds
import handlers.tournament_mode.next_round
import handlers.tournament_mode.end

if __name__ == "__main__":
    bot.run()
