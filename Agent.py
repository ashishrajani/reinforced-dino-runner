from Game import Game


class Agent:

    def __init__(self, game: Game):
        # takes game as input for taking actions
        self._game = game

        # to start the game, we need to jump once
        self.jump()

    def is_running(self):
        # return true if game is in progress, false is crashed or paused

        return self._game.is_playing()

    def is_crashed(self):
        # return true if the agent as crashed on an obstacles. Gets javascript variable from game describing the state

        return self._game.is_crashed()

    def jump(self):
        # make agent jump

        self._game.press_up()

    def duck(self):
        # make agent duck

        self._game.press_down()
