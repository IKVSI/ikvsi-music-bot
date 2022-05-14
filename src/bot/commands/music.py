from aiogram import types, Bot
from .commands import Commands
from .states import Music, Base
from ..db import base
from ..templates import Templates


class MusicAddCommands(Commands):
    def __init__(self, **kwargs):
        super().__init__(state=Music.add.state)

    def initHandlers(self):
        self.handler = Commands.dispatcher.message_handler

        @self.register(content_types=["audio"])
        async def get_music(message: types.Message):
            context = self.dispatcher.current_state(
                chat=message.chat.id, user=message.from_user.id
            )
            await context.update_data(music_message_id=message.message_id)
            await Music.title.set()
            await message.answer(Templates.music_title)

        get_music.description = "ожидается музыкальный файл"


class MusicTitleCommands(Commands):
    def __init__(self, **kwargs):
        super().__init__(state=Music.title.state)

    def initHandlers(self):
        self.handler = self.dispatcher.message_handler

        @self.register()
        async def get_title(message: types.Message):
            context = self.dispatcher.current_state(
                chat=message.chat.id, user=message.from_user.id
            )
            await context.update_data(title=message.text)
            await Music.artist.set()
            info_list = [""]
            for commands, info in Commands.commands_for_state(Music.artist.state):
                info_list.append(
                    Templates.commands_info.format(commands=commands, description=info)
                )
            await message.answer(
                Templates.music_artist.format(info=Templates.indent.join(info_list)),
                parse_mode=types.ParseMode.MARKDOWN_V2,
            )

        get_title.description = "ожидается название трэка"


class MusicArtistCommands(Commands):
    def __init__(self, **kwargs):
        super().__init__(state=Music.artist.state)

    def initHandlers(self):
        self.handler = Commands.dispatcher.message_handler

        @self.register(commands=["new_artist"])
        async def new_artist(message: types.Message):
            context = Commands.dispatcher.current_state(
                chat=message.chat.id, user=message.from_user.id
            )
            await context.update_data(new=True)
            await Music.new_artist.set()
            await message.answer(Templates.music_new_artist)

        new_artist.description = "добавим нового артиста"

        @self.register(commands=["list_artists"])
        async def list_artists(message: types.Message):
            await Music.list_artists.set()

        list_artists.description = "выберем артиста из имеющихся"


async def finish_add_track(bot: Bot, data: dict, chat_id: int):
    await bot.forward_message(
        chat_id=chat_id, from_chat_id=chat_id, message_id=data["music_message_id"]
    )
    await bot.send_message(
        chat_id=data["chat_id"],
        text=Templates.music_finish_add.format(**data),
        parse_mode=types.ParseMode.MARKDOWN_V2,
    )


class MusicNewArtistCommands(Commands):
    def __init__(self, **kwargs):
        super().__init__(state=Music.new_artist.state)

    def initHandlers(self):
        self.handler = Commands.dispatcher.message_handler

        @self.register()
        async def get_new_artist(message: types.Message):
            context = Commands.dispatcher.current_state(
                chat=message.chat.id, user=message.from_user.id
            )
            await context.update_data(artist=message.text, chat_id=message.chat.id)
            await Music.finish.set()
            await finish_add_track(
                bot=Commands.dispatcher.bot,
                data=await context.get_data(),
                chat_id=message.chat.id,
            )

        get_new_artist.description = "ожидается имя артиста / название группы"


class MusicFinishCommands(Commands):
    def __init__(self, **kwargs):
        super().__init__(state=Music.finish.state)

    def initHandlers(self):
        self.handler = Commands.dispatcher.message_handler

        @self.register(commands=["yes"])
        async def yes(message: types.Message):
            context = Commands.dispatcher.current_state(
                chat=message.chat.id, user=message.from_user.id
            )
            data = await context.get_data()
            user = message.from_user
            music_message = await Commands.dispatcher.bot.forward_message(
                chat_id=Commands.storage_chat_id.get_secret_value(),
                from_chat_id=message.chat.id,
                message_id=data["music_message_id"],
            )

            def sync(session):
                if data["new"]:
                    artist = base.Lists(
                        list_name=data["artist"],
                        user_id=user.id,
                        list_type=base.ListEnum.artist,
                    )
                    session.add(artist)
                    session.flush()
                    session.refresh(artist)
                session.add(
                    base.Songs(title=data["title"], song_id=music_message.message_id)
                )
                library: base.Lists = (
                    session.query(base.Lists)
                    .where(user.id == base.Lists.user_id)
                    .where("Library" == base.Lists.list_name)
                    .where(base.ListEnum.default == base.Lists.list_type)
                    .first()
                )
                session.add(
                    base.Binds(
                        list_id=library.list_id, song_id=music_message.message_id
                    )
                )
                session.add(
                    base.Binds(list_id=artist.list_id, song_id=music_message.message_id)
                )
                session.commit()

            async with Commands.async_session() as session:
                answer = await session.run_sync(sync)
            await message.answer(Templates.music_yes)

        @self.register(commands=["no"])
        async def no(message: types.Message):
            context = Commands.dispatcher.current_state(
                chat=message.chat.id, user=message.from_user.id
            )
            await context.reset_data()
            await Base.root.set()
            await message.answer(Templates.music_no)
            await Commands.registered_commands["*"]["/help"](message)


MusicCommands = [
    MusicAddCommands,
    MusicTitleCommands,
    MusicArtistCommands,
    MusicNewArtistCommands,
    MusicFinishCommands,
]
