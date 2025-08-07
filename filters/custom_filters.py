from pyrogram.types import Message
from pyrogram.filters import Filter
from games.state_manager import get_game

class IsReferee(Filter):
    async def __call__(self, _, message: Message):
        game = get_game(message.chat.id)
        if not game:
            return False
        return message.from_user.id == game.get("referee")

is_referee = IsReferee()
