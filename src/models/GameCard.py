from typing import Optional

from models.GameDetails import GameDetails
from models.GameUsage import GameUsage

class GameCard:
    """The data used by a GameCard
    """
    def __init__(self, game:GameDetails, game_usage:Optional[GameUsage]=None):
        self._game = game
        self._game_usage = game_usage
        self._game_link = f"gamedata.html?game={game.ID}"
        self._monthly_sessions = GameCard._to_kilo(game_usage.AverageMonthlySessions()) if game_usage else "0"

    def __str__(self):
        return f"GameCard: {self.Game}; {self.MonthlySessions} Session Avg"

    def __repr__(self):
        return f"GameCard: game={self.Game} usage=<{self.GameUsage}> sessions={self.MonthlySessions}"

    # get methods
    @property
    def Game(self) -> GameDetails:
        return self._game
    @property
    def GameUsage(self) -> Optional[GameUsage]:
        return self._game_usage
    @property
    def GameLink(self) -> str:
        return self._game_link
    @property
    def MonthlySessions(self) -> str:
        return self._monthly_sessions

    @staticmethod
    def _to_kilo ( num:int | float ) -> str:
        """ Round number to kilos (nearest 1K)

        :param num: The number to format as number of kilos
        :type num: int|float
        :return: Returns number in kilos or the number passed if under 1K 
        :rtype: str
        """
        return str(num) if (num < 1000) else f"{round(num/1000)}K"
