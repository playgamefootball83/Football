from pyrogram import filters
from pyrogram.types import Message
from bot import bot
from games.state_manager import get_game, update_game
from pyrogram.enums import ChatMemberStatus


def register_handlers(bot):
    @bot.on_message(filters.command(["assign_captain", "assign_goalkeeper"]) & filters.group)
    async def assign_role(_, message: Message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        game = get_game(chat_id)

        if not game or not game.get("active") or game.get("mode") != "team_mode":
            await message.reply("❌ Koi active team match nahi hai.")
            return

        if user_id != game.get("referee"):
            await message.reply("❌ Sirf referee hi role assign kar sakta hai.")
            return

        if not message.reply_to_message:
            await message.reply("⚠️ Kisi player ko reply karke ye command use karo.")
            return

        target_user = message.reply_to_message.from_user
        target_id = target_user.id
        target_name = target_user.first_name

        role_type = "captain" if "captain" in message.command[0] else "goalkeeper"
        team = None

        # Find the player's team
        for t in ["A", "B"]:
            if target_id in game["teams"][t]:
                team = t
                break

        if not team:
            await message.reply("❌ Ye player kisi bhi team me nahi hai.")
            return

        if game["roles"][team][role_type]:
            await message.reply(f"⚠️ Team {team} ka {role_type} pehle se assigned hai.")
            return

        # Assign the role
        game["roles"][team][role_type] = target_id
        update_game(chat_id, game)

        await message.reply(
            f"🎖️ Assigned **{role_type.capitalize()}** of Team {team} to [{target_name}](tg://user?id={target_id})!"
        )
