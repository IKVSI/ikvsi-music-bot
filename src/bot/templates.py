from pydantic import BaseSettings


class Templates:
    greeting: str = "Привет, Я бот!"
    state_info: str = "Твоё текущее состояние {state}!"
