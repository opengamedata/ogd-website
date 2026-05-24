from typing import Optional

from ogd.apis.models.files.GameSummaries import GameSummary

from models.GameDetails import GameDetails

class GameCard:
    """The data used by a GameCard
    """
    def __init__(self, game:GameDetails, game_data_summary:Optional[GameSummary]=None):
        self._game = game
        self._game_data_summary = game_data_summary
        self._game_link = f"gamedata.html?game={game.ID}"
        self._monthly_sessions = game_data_summary.AverageSessionCount if game_data_summary else None

    def __str__(self):
        return f"GameCard: {self.Game}; {self.MonthlySessions} Session Avg"

    def __repr__(self):
        return f"GameCard: game={self.Game} usage=<{self.GameDataSummary}> sessions={self.MonthlySessions}"

    # get methods
    @property
    def Game(self) -> GameDetails:
        return self._game
    @property
    def GameDataSummary(self) -> Optional[GameSummary]:
        return self._game_data_summary
    @property
    def GameLink(self) -> str:
        return self._game_link
    @property
    def MonthlySessions(self) -> Optional[int]:
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
