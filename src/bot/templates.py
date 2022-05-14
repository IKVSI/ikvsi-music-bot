from pydantic import BaseSettings
from aiogram.utils import markdown
from aiogram import types


class Templates:
    greeting = "Привет @{user_name}, Я музыкальный бот @{bot_name}! Хочешь создать свою музыкальную библиотеку?"
    greeting_for_old = "Привen @{user_name}, пришёл послушать музыку?"
    reset = "@{user_name}, произошёл сброс в исходное состояние."
    state_info = "Твоё текущее состояние {state}!"
    list_playlists = "Вот все твои плэйлисты:{playlists}"
    indent = "\n    • "
    commands_info = "{commands} \- {description}"
    waiters_info = "{description}"
    help_info = "В состоянии *{state}* работают команды или ожидаются: {info}"
    music_add = "Давай добавим трэк, отправь мне музыкальный файл."
    music_title = "Добавим название для трэка?"
    music_artist = "Добавим артиста для трэка? Используй команды: {info}"
    music_new_artist = "Добавим артиста?"
    music_finish_add = (
        "Добавляем?\n    • Artist: {artist}\n    • Track: {title}\n  /yes        /no"
    )
    music_yes = "Трэк добавлен :)"
    music_no = "Ну и не нужен этот трэк!"
    default_description = "Хрен знает что делает :/"
