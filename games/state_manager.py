# Memory-based game storage

game_states = {}  # { chat_id: {...} }

def create_game(chat_id: int, referee_id: int):
    game_states[chat_id] = {
        "referee": referee_id,
        "teams": {},  # { "A": [user_id, ...], ... }
        "roles": {},  # { user_id: "captain"/"goalkeeper" }
        "round": 0,
        "active": True,
        "actions": {},  # for each round
        "cards": {},  # yellow/red card record
        "mode": "team",  # later: tournament
    }

def is_game_running(chat_id: int) -> bool:
    return chat_id in game_states and game_states[chat_id].get("active", False)

def get_game(chat_id: int):
    return game_states.get(chat_id)

def end_game(chat_id: int):
    if chat_id in game_states:
        game_states[chat_id]["active"] = False
