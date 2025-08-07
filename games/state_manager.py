active_games = {}

def create_game(chat_id, game_data):
    games[chat_id] = game_data

def get_game(chat_id):
    return games.get(chat_id)

def update_game(chat_id, new_data):
    if chat_id in games:
        games[chat_id].update(new_data)

def delete_game(chat_id):
    if chat_id in games:
        del games[chat_id]
