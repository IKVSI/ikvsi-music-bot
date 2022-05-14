from aiogram.dispatcher.filters.state import State, StatesGroup


class Base(StatesGroup):
    root = State()


class Music(StatesGroup):
    add = State()
    title = State()
    artist = State()
    new_artist = State()
    list_artists = State()
    finish = State()
