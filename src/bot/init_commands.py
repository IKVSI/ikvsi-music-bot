from .commands import Commands
from .states import States


class InitCommands(Commands):
    def __init__(self, dispatcher):
        super().__init__(state=States.INIT, dispatcher=dispatcher)

    def initCommands(self):
        pass
