from aiogram import types
from sqlalchemy.future import select

from .commands import Commands
from .states import Base, Music
from ..db import base
from ..templates import Templates


class RootCommands(Commands):
    def __init__(self, **kwargs):
        super().__init__(state=Base.root.state)

    def initHandlers(self):
        self.handler = Commands.dispatcher.message_handler

        @self.register(commands=["all_lists"])
        async def all_lists(message: types.Message):
            user = message.from_user
            result = []
            async with Commands.async_session() as session:
                result = list(
                    f"*{playlist[0].list_name}* \\({playlist[0].list_type.value}\\)"
                    for playlist in await session.execute(
                        select(base.Lists)
                        .where(user.id == base.Lists.user_id)
                        .order_by(base.Lists.list_id)
                    )
                )
                await session.commit()
            await message.answer(
                Templates.list_playlists.format(
                    playlists="\n    • {}".format("\n    • ".join(result))
                ),
                parse_mode=types.ParseMode.MARKDOWN_V2,
            )

        all_lists.description = "показыает все плэйлисты пользователя"

        @self.register(commands=["add", "add_music"])
        async def add_music(message: types.Message):
            await Music.add.set()
            await message.answer(Templates.music_add)

        add_music.description = "добавляет трэк в библиотеку"
