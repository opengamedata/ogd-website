from models.GameDetails import GameDetails
from models.GameUsage import GameUsage

class GameCard:
    """The data used by a GameCard
    
    TODO: kick this stupid structure to the curb, pass the other two objects separately. We're not saving much with this.
    """
    def __init__(self, game:GameDetails, game_usage:GameUsage):
        self._game = game
        self._game_usage = game_usage

    # get methods
    def getGame(self) -> GameDetails:
        return self._game
    def getGameUsage(self) -> GameUsage:
        return self._game_usage
