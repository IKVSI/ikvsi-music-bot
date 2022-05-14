from aiogram import types
from aiogram.utils import markdown

from ..db import base
from ..templates import Templates
from .states import Base
from .commands import Commands


class OverstateCommands(Commands):
    def __init__(self, **kwargs):
        super().__init__(state="*")

    def initHandlers(self):
        self.handler = Commands.dispatcher.message_handler

        @self.register(commands=["start"])
        async def start(message: types.Message):
            user = message.from_user
            context = Commands.dispatcher.current_state(
                chat=message.chat.id, user=user.id
            )
            state = await context.get_state()
            if (state is None) or (state == Base.root.state):

                def sync(session):
                    result: base.Users = (
                        session.query(base.Users)
                        .where(user.id == base.Users.user_id)
                        .one_or_none()
                    )
                    if result:
                        if result.user_name != user.username:
                            result.user_name = user.username
                        return Templates.greeting_for_old
                    else:
                        session.add(
                            base.Users(user_id=user.id, user_name=user.username)
                        )
                        session.flush()
                        session.add(
                            base.Lists(
                                list_name="Library",
                                user_id=user.id,
                                list_type=base.ListEnum.default,
                            )
                        )
                        session.commit()
                        return Templates.greeting

                async with Commands.async_session() as session:
                    answer = await session.run_sync(sync)
            else:
                answer = Templates.reset
            if await context.get_data():
                await context.reset_data()
            await Base.root.set()
            await message.answer(
                answer.format(
                    user_name=user.username,
                    bot_name=(await Commands.dispatcher.bot.get_me()).username,
                )
            )

        start.description = f"сброс бота в начальное состояние {Base.root.state}"

        @self.register(commands=["help"])
        async def help(message: types.Message):
            context = Commands.dispatcher.current_state(
                chat=message.chat.id, user=message.from_user.id
            )
            state = await context.get_state()
            info_list = [""]
            for info in Commands.waiters_for_state(state):
                info_list.append(Templates.waiters_info.format(description=info))
            for info in Commands.waiters_for_state("*"):
                info_list.append(Templates.waiters_info.format(description=info))
            for commands, info in Commands.commands_for_state(state):
                info_list.append(
                    Templates.commands_info.format(commands=commands, description=info)
                )
            for commands, info in Commands.commands_for_state("*"):
                info_list.append(
                    Templates.commands_info.format(commands=commands, description=info)
                )

            answer = markdown.text(
                Templates.help_info.format(
                    state=await Commands.dispatcher.current_state().get_state(),
                    info=Templates.indent.join(info_list),
                )
            )
            await message.answer(answer, parse_mode=types.ParseMode.MARKDOWN_V2)

        help.description = "показывает возможные команды в текущем состоянии"
