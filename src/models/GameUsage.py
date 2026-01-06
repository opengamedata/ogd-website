import json
from typing import List, Optional

from ogd.common.utils.typing import Map

class MonthSessions:
    """Direct representation of the data structures from the legacy ‎‎MonthlyGameUsage endpoint. 
    """
    def __init__(self, year:int, month:int, total_sessions:int):
        self._year = year
        self._month = month
        self._total_sessions = total_sessions

    @property
    def Year(self) -> int:
        return self._year
    @property
    def Month(self) -> int:
        return self._month
    @property
    def TotalSessions(self) -> int:
        return self._total_sessions

class GameUsage:
    """An aggregate of the month-by-month usage stats for a single game.
    """
    def __init__(self, game_id:Optional[str], months:List[MonthSessions]):
        self._game_id = game_id
        self._months = months

    @staticmethod
    def FromDict(obj:Map):
        return GameUsage(
            game_id  = obj.get("game_id"),
            months = obj.get("sessions", [])
        )

    @staticmethod
    def FromJson(raw_json):
        obj = json.loads(raw_json)
        return GameUsage.FromDict(obj)

    # get methods
    @property
    def ID(self):
        return self._game_id
    @property
    def Months(self) -> List[MonthSessions]:
        return self._months
    @property
    def Sessions(self) -> List[MonthSessions]:
        """Alias for Months property

        :return: _description_
        :rtype: List[MonthSessions]
        """
        return self.Months
    @property
    def LatestMonthlySessions(self):
        return self.Months[-1].TotalSessions if len(self.Months) > 0 else 0

    def AverageMonthlySessions(self, month_range:int=12) -> int:
        """Calculate the average number of monthly gameplay sessions over a range of months.
        
        First, finds the most-recent month that had sessions
        Then sums up the number of sessions in that month and previous months,
        going back up to `month_range` months.

        :param month_range: The maximum range over which to calculate the average, defaults to 12
        :type month_range: int, optional
        :return: The average number of sessions per month over the given range
        :rtype: int
        """
        ret_val = 0

        months_counted = 0
        sum_sessions   = 0

        # Loop through months from most recent to oldest
        for month in reversed(self._months):
            # If this month has sessions
            if month.TotalSessions > 0:
                # Add it to our sum
                sum_sessions += month.TotalSessions
            # If we've found a month with sessions either this iteration or a previous iteration
            if sum_sessions > 0:
                # This month counts towards our 12 whether or not it had sessions
                months_counted += 1
            # Once we have 12 months of data we can quit
            if months_counted == month_range:
                break

        # If we counted at least one month
        if months_counted > 0:
            # Return an integer average
            ret_val = (int)(sum_sessions / months_counted)

        return ret_val