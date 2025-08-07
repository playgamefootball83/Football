def save_action(chat_id, round_number, user_id, action):
    from .state_manager import get_game
    game = get_game(chat_id)
    game["actions"][round_number][user_id] = action
