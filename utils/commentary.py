import random

def get_commentary(action, player_name, opponent_name=None):
    if action == "KICK":
        return random.choice([
            f"⚽ {player_name} shoots straight at the goal!",
            f"🔥 {player_name} with a powerful kick!",
            f"🚀 {player_name} goes for goal!",
            f"🎯 {player_name} attempts a perfect strike!"
        ])
    elif action == "PASS":
        return random.choice([
            f"🔁 {player_name} passes the ball cleverly!",
            f"📦 {player_name} makes a smooth pass.",
            f"🎯 {player_name} finds a teammate with a quick pass.",
            f"🤝 {player_name} connects a perfect pass!"
        ])
    elif action == "DEFENSIVE":
        return random.choice([
            f"🛡 {player_name} blocks the attack like a wall!",
            f"🧱 {player_name} intercepts the ball smartly.",
            f"🕴 {player_name} reads the game beautifully and stops the attack.",
            f"💪 {player_name} tackles with precision!"
        ])
    elif action == "GOAL":
        return f"🥅 GOAL! {player_name} scores with a brilliant finish!"

    elif action == "SAVE":
        return f"🧤 Great save by {player_name}! The crowd goes wild!"

    elif action == "INTERCEPT":
        return f"🚫 {player_name} intercepts {opponent_name}'s move and takes control!"

    return f"{player_name} makes a move!"
