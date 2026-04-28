import json
from typing import List, Optional

from ogd.common.utils.typing import Map

class MonthSessions:
    """Direct representation of the data structures from the legacy ‎‎MonthlyGameUsage endpoint. 
    """
    def __init__(self, year:int, month:int, total_sessions:Optional[int]):
        self._year           : int           = year
        self._month          : int           = month
        self._total_sessions : Optional[int] = total_sessions

    def __str__(self):
        return f"{self.Year}/{self.Month}: {self.TotalSessions} sessions"

    def __repr__(self):
        return f"MonthSessions: {self}"

    @staticmethod
    def FromDict(obj:Map):
        if isinstance(obj, MonthSessions):
            return obj
        elif isinstance(obj, dict):
            return MonthSessions(
                year           = obj.get("year", None),
                month          = obj.get("month", None),
                total_sessions = obj.get("total_sessions", 0)
            )
        else:
            raise TypeError(f"MonthSessions.FromDict was given invalid object, with type {type(obj)}")

    @property
    def Year(self) -> int:
        return self._year
    @property
    def Month(self) -> int:
        return self._month
    @property
    def TotalSessions(self) -> Optional[int]:
        return self._total_sessions

class GameUsage:
    """An aggregate of the month-by-month usage stats for a single game.
    """
    def __init__(self, game_id:Optional[str], months:List[MonthSessions]):
        self._game_id = game_id
        self._months = months

    def __str__(self):
        return f"{self.ID} usage {self.Months[0].Year}/{self.Months[0].Month}-{self.Months[1].Year}/{self.Months[1].Month}"

    def __repr__(self):
        return f"GameUsage: {self.ID} from {self.Months[0].Year}/{self.Months[0].Month}-{self.Months[1].Year}/{self.Months[1].Month}"

    @staticmethod
    def FromDict(raw_dict:Map):
        if not isinstance(raw_dict, dict):
            print(f"GameUsage was asked to use an object of type {type(raw_dict)} for parsing, with value:\n'{raw_dict}'\nAttempting to load as json")
            raw_dict = json.loads(str(raw_dict))
        _months = raw_dict.get("sessions", [])
        return GameUsage(
            game_id  = raw_dict.get("game_id"),
            months = [MonthSessions.FromDict(month) for month in _months]
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
            if month.TotalSessions and month.TotalSessions > 0:
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