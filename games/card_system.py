def give_yellow_card(chat_id, user_id):
    from .state_manager import get_game
    game = get_game(chat_id)

    if user_id not in game["cards"]:
        game["cards"][user_id] = {"yellow": 0, "red": 0}

    game["cards"][user_id]["yellow"] += 1

    # Auto red on 2 yellow
    if game["cards"][user_id]["yellow"] >= 2:
        game["cards"][user_id]["red"] += 1
