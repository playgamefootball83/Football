from bot import bot

# Match Setup
import handlers.match_setup.select_mode
import handlers.match_setup.team_mode_handler
import handlers.match_setup.tournament_mode_handler

# Team Mode
import handlers.team_mode.kickoff
import handlers.team_mode.rounds
import handlers.team_mode.next_round

# Tournament Mode
import handlers.tournament_mode.kickoff
import handlers.tournament_mode.rounds
import handlers.tournament_mode.next_round

# Shared Handlers
import handlers.shared.end_game

bot.run()
