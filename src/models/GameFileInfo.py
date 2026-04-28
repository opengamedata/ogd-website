import html
import json
from datetime import date
from typing import Dict, List, Optional

from dateutil.relativedelta import relativedelta

from config.AppConfig import AppConfig

class GameFileInfo:
    """GameFileInfo
        Realistically, should be named DatasetInfo
        Contains all data for modeling a dataset, including date range, and links to files, templates, and generator code.
    """
    def __init__(self, game_id:Optional[str],
                 first_month:Optional[int],   first_year:Optional[int],
                 last_month:Optional[int],    last_year:Optional[int],
                 found_matching_range:Optional[bool],
                 raw_file        : Optional[str]=None,
                 events_file     : Optional[str]=None, events_template     : Optional[str]=None,
                 sessions_file   : Optional[str]=None, sessions_template   : Optional[str]=None,
                 players_file    : Optional[str]=None, players_template    : Optional[str]=None,
                 population_file : Optional[str]=None, population_template : Optional[str]=None,
                 detectors_link  : Optional[str]=None, features_link       : Optional[str]=None):
        self._game_id              = game_id
        self._first_month          = first_month
        self._first_year           = first_year
        self._last_month           = last_month
        self._last_year            = last_year
        self._found_matching_range = found_matching_range
        self._raw_file             = raw_file
        self._events_file          = events_file
        self._events_template      = events_template
        self._sessions_file        = sessions_file
        self._sessions_template    = sessions_template
        self._players_file         = players_file
        self._players_template     = players_template
        self._population_file      = population_file
        self._population_template  = population_template
        self._detectors_link       = detectors_link
        self._features_link        = features_link

    @staticmethod
    def FromDict(raw_dict:Dict, game_id:Optional[str]):
        if not isinstance(raw_dict, dict):
            print(f"GameFileInfo was asked to use an object of type {type(raw_dict)} for parsing, with value:\n'{raw_dict}'\nAttempting to load as json")
            raw_dict = json.loads(str(raw_dict))
        return GameFileInfo(
            game_id              = game_id if game_id else raw_dict.get('game_id', "UNKNOWN"),
            first_month          = raw_dict.get('first_month'),
            first_year           = raw_dict.get('first_year'),
            last_year            = raw_dict.get('last_year'),
            last_month           = raw_dict.get('last_month'),
            found_matching_range = raw_dict.get('found_matching_range'),
            events_file          = raw_dict.get('events_file'),
            events_template      = raw_dict.get('events_template'),
            players_file         = raw_dict.get('players_file'),
            players_template     = raw_dict.get('players_template'),
            population_file      = raw_dict.get('population_file'),
            population_template  = raw_dict.get('population_template'),
            raw_file             = raw_dict.get('raw_file'),
            sessions_file        = raw_dict.get('sessions_file'),
            sessions_template    = raw_dict.get('sessions_template'),
            detectors_link       = raw_dict.get('detectors_link'),
            features_link        = raw_dict.get('features_link')
        )

    # Get methods
    @property
    def GameID(self) -> Optional[str]:
        return self._game_id
    @property
    def FirstMonth(self) -> Optional[int]:
        return self._first_month
    @property
    def FirstYear(self) -> Optional[int]:
        return self._first_year
    @property
    def FirstDate(self) -> Optional[date]:
        ret_val = None

        if self.FirstYear and self.FirstMonth:
            ret_val = date(year=self.FirstYear, month=self.FirstMonth, day=1)

        return ret_val
    @property
    def LastMonth(self) -> Optional[int]:
        return self._last_month
    @property
    def LastYear(self) -> Optional[int]:
        return self._last_year
    @property
    def LastDate(self) -> Optional[date]:
        ret_val = None

        if self.LastYear and self.LastMonth:
            ret_val = date(year=self.LastYear, month=self.LastMonth, day=1)

        return ret_val
    @property
    def FoundRange(self):
        return str(self._found_matching_range)
    @property
    def RawFileLink(self, html_safe:bool=True) -> Optional[str]:
        return html.escape(str(self._raw_file), quote=True) if html_safe else self._raw_file
    @property
    def EventsFileLink(self, html_safe:bool=True) -> Optional[str]:
        return html.escape(str(self._events_file), quote=True) if html_safe else self._events_file
    @property
    def EventsTemplateLink(self, html_safe:bool=True) -> Optional[str]:
        return html.escape(str(self._events_template), quote=True) if html_safe else self._events_template
    @property
    def PlayersFileLink(self, html_safe:bool=True) -> Optional[str]:
        return html.escape(str(self._players_file), quote=True) if html_safe else self._players_file
    @property
    def PlayersTemplateLink(self, html_safe:bool=True) -> Optional[str]:
        return html.escape(str(self._players_template), quote=True) if html_safe else self._players_template
    @property
    def PlayersDashboardLink(self, html_safe:bool=True) -> Optional[str]:
        dash_base = AppConfig.APP_CONFIG.get("DASHBOARD_URL_BASE")
        dash_url  = f"{dash_base}?game={self.GameID}&year={self.FirstYear}&month={self.FirstMonth}&level=player"
        return html.escape(dash_url, quote=True) if html_safe else dash_url
    @property
    def PopulationFileLink(self, html_safe:bool=True) -> Optional[str]:
        return html.escape(str(self._population_file), quote=True) if html_safe else self._population_file
    @property
    def PopulationTemplateLink(self, html_safe:bool=True) -> Optional[str]:
        return html.escape(str(self._population_template), quote=True) if html_safe else self._population_template
    @property
    def PopulationDashboardLink(self, html_safe:bool=True) -> Optional[str]:
        dash_base = AppConfig.APP_CONFIG.get("DASHBOARD_URL_BASE")
        dash_url  = f"{dash_base}?game={self.GameID}&year={self.FirstYear}&month={self.FirstMonth}&level=population"
        return html.escape(dash_url, quote=True) if html_safe else dash_url
    @property
    def SessionsFileLink(self, html_safe:bool=True) -> Optional[str]:
        return html.escape(str(self._sessions_file), quote=True) if html_safe else self._sessions_file
    @property
    def SessionsTemplateLink(self, html_safe:bool=True) -> Optional[str]:
        return html.escape(str(self._sessions_template), quote=True) if html_safe else self._sessions_template
    @property
    def FeatureFiles(self):
        return {
            "Population Features":self.PopulationFileLink,
            "Player Features":self.PlayersFileLink,
            "Session Features":self.SessionsFileLink,
        }

    @property
    def DetectorsLink(self, html_safe:bool=True) -> Optional[str]:
        return html.escape(str(self._detectors_link), quote=True) if html_safe else self._detectors_link

    @property
    def FeaturesLink(self, html_safe:bool=True) -> Optional[str]:
        return html.escape(str(self._features_link), quote=True) if html_safe else self._features_link

    @property
    def HasNoFiles(self) -> bool:
        return self.RawFileLink is None \
           and self.EventsFileLink is None \
           and self.DetectorsLink is None \
           and self.FeaturesLink is None \
           and self.FeatureFiles is None

    # Prev/next month functions

    @property
    def UsageRange(self) -> List[date]:
        """ Get range of dates from first month/year to last month/year
        
        :return: array of DateTime objects
        :rtype: Optional[str]
        """
        ret_val : List[date] = []

        if self.FirstDate and self.LastDate:
            current_date = self.FirstDate
            while current_date <= self.LastDate:
                ret_val.append(current_date)
                current_date += relativedelta(month=1)

        return ret_val

    def GetPrevMonth(self, selected_date:date) -> date:
        """Get the previous month

        Returns previous month number or selected month if no previous month exists

        TODO : simplify, pretty sure this could just be:
        try:
            usage_range = self.UsageRange
            idx = usage_range.index(selected_date)
        except ValueError:
            return selected_date
        else
            return usage_range[idx-1] if idx > 0 else selected_date

        99% sure checking that idx+1 <= count is pointless, inherited logic from a bad initial implementation.
        Possibly a bad copy-paste up from the getNextMonth logic?

        :param current_date: _description_
        :type current_date: date
        :return: _description_
        :rtype: _type_
        """
        if self.FirstDate == selected_date:
            return selected_date

        # If date not found, return selected_date
        usage_range = self.UsageRange
        if selected_date not in usage_range:
            return selected_date

        # Return previous month from usage_range
        idx = usage_range.index(selected_date)
        return usage_range[idx-1] if idx+1 <= len(usage_range) else selected_date

    def GetNextMonth(self, current_date:date) -> date:
        """/* Get the next month
        * Returns next month number or selected month if no next month exists
        * <param> DateTime selected_date
        */"""
        if self.LastDate == current_date:
            return current_date

        usage_range = self.UsageRange

        # If date not found, return selected_date
        if current_date not in usage_range:
            return current_date

        # Return next month from usage_range
        idx = usage_range.index(current_date)
        return usage_range[idx+1] if idx < len(usage_range) else current_date
