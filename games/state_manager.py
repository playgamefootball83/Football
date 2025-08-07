# This dictionary will hold all active games
active_games = {}

def create_game(chat_id, game_data):
    active_games[chat_id] = game_data

def get_game(chat_id):
    return active_games.get(chat_id)

def update_game(chat_id, new_data):
    if chat_id in active_games:
        active_games[chat_id].update(new_data)

def delete_game(chat_id):
    if chat_id in active_games:
        del active_games[chat_id]
