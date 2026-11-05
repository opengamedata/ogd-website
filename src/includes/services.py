from pathlib import Path
from typing import Dict, Optional

from flask import current_app

from ogd.common.utils.fileio import loadJSONFile
from ogd.common.utils.typing import Map
from ogd.apis.models.APIRequest import APIRequest
from ogd.apis.models.APIResponse import APIResponse
from ogd.apis.models.enums.ResponseStatus import ResponseStatus
from ogd.apis.models.enums.RESTType import RESTType
from ogd.apis.models.files.GameSummary import GameSummary
from ogd.apis.models.files.GameSummaries import GameSummaries
from ogd.apis.utils.APIUtils import urljoin

from config.AppConfig import AppConfig
# from models.APIResponse import APIResponse
from models.GameDetails import GameDetails
from models.GameFileInfo import GameFileInfo

def getGameList() -> Dict[str, GameDetails]:
    """ Get Games from game_list
        
        TODO : remove, we can just use the loadJSONFile function.

        Returns list or False
    """ 
    game_list = loadJSONFile(filename='game_list.json', path=Path("./config/"))
    print(f"Found the following for game list:\n{game_list}")
    return {game_id:GameDetails.FromDict(game_id=game_id, raw_dict=game_details) for game_id,game_details in game_list.items()}

def getGameDetails(game_id:str) -> Optional[GameDetails]:
    """ Get single game details from game_list
    * <param> string game_id
    * Returns Array object associated with given game_id or None
    """
    # Get full list of games
    game_list = getGameList()
    # API will return just one game, for now access game_id and return contents
    return game_list.get(game_id)

# def getGameSummaries() -> Dict[str, GameSummary]:
#     ret_val = None

#     url = urljoin(base=AppConfig.APP_CONFIG.get('WEBSITE_API_URL_BASE', "http://localhost:5000"), url=GameSummary.PATH)
#     api_response = APIRequest(url=url, request_type=RESTType.GET, params={}).Execute(current_app.logger)

#     if api_response:
#         if api_response.Status == ResponseStatus.OK:
#             if api_response.Value:
#                 ret_val = {key:GameSummary.FromAPIResponse() for key,val in api_response.Value.items()}
#             else:
#                 err_str = f"getGameUsageByMonth request, for game_id={game_id} with year={year} and month={month}, had empty value element!:\nResponse message: {api_response.Message}"
#                 current_app.logger.error(err_str)
#         else:
#             err_str = f"getGameUsageByMonth request, for game_id={game_id} with year={year} and month={month}, was unsuccessful:\n{api_response.Message}"
#             current_app.logger.error(err_str)
#     else:
#         err_str = f"getGameUsageByMonth request, for game_id={game_id} with year={year} and month={month}, got no response object!"
#         current_app.logger.error(err_str)

# def getGameUsageByMonth(game_id:str, year:Optional[int] = None, month : Optional[int] = None) -> Optional[GameUsage]:
#     """ Get game usage from API
#     * <param> string game_id
#     * <param> string year - optional
#     * <param> string month - optional
#     """
#     ret_val = None

#     params = {
#         'game_id': game_id,
#         'year'   : year,
#         'month'  : month
#     }

#     # 1. Make request to API
#     usage_url = urljoin(base=AppConfig.APP_CONFIG.get('WEBSITE_API_URL_BASE', "http://localhost:5000"), url="getGameUsageByMonth")
#     api_response = APIRequest(url=usage_url, request_type=RESTType.GET, params=params).Execute(current_app.logger)

#     # 2. Convert response to a GameUsage object
#     if api_response:
#         if api_response.Status == ResponseStatus.OK:
#             if api_response.Value:
#                 ret_val = GameUsage.FromDict(api_response.Value)
#             else:
#                 err_str = f"getGameUsageByMonth request, for game_id={game_id} with year={year} and month={month}, had empty value element!:\nResponse message: {api_response.Message}"
#                 current_app.logger.error(err_str)
#         else:
#             err_str = f"getGameUsageByMonth request, for game_id={game_id} with year={year} and month={month}, was unsuccessful:\n{api_response.Message}"
#             current_app.logger.error(err_str)
#     else:
#         err_str = f"getGameUsageByMonth request, for game_id={game_id} with year={year} and month={month}, got no response object!"
#         current_app.logger.error(err_str)

#     return ret_val

# def getGameFileInfoByMonth(game_id:str, year:Optional[int]=None, month:Optional[int]=None) -> Optional[GameFileInfo]:
#     """ Get game file info from API
#     * <param> string game_id
#     * <param> string year --optional
#     * <param> string month --optional
#     """
#     ret_val = None

#     params = {
#         'game_id' : game_id,
#         'year' : year,
#         'month' : month
#     }
    
#     # 1. Make request to API via cURL
#     info_url = urljoin(base=AppConfig.APP_CONFIG.get('WEBSITE_API_URL_BASE', "http://localhost:5000"), url="getGameFileInfoByMonth")
#     api_response : APIResponse = APIRequest(url=info_url, request_type=RESTType.GET, params=params, timeout=5).Execute(current_app.logger)

#     # 2. Convert response to a GameFileInfo object
#     if api_response:
#         if api_response.Status == ResponseStatus.OK:
#             if api_response.Value:
#                 ret_val = GameFileInfo.FromDict(api_response.Value, game_id=game_id)
#             else:
#                 err_str = f"getGameFileInfoByMonth request, for game_id={game_id} with year={year} and month={month}, had empty value element!\nResponse message: {api_response.Message}"
#                 current_app.logger.error(err_str)
#         else:
#             err_str = f"getGameFileInfoByMonth request, for game_id={game_id} with year={year} and month={month}, was unsuccessful:\n{api_response.Message}"
#             current_app.logger.error(err_str)
#     else:
#         err_str = f"getGameFileInfoByMonth request, for game_id={game_id} with year={year} and month={month}, got no response object!"
#         current_app.logger.error(err_str)

#     return ret_val

# def getGameUsage(game_id:str) -> Optional[GameUsage]:
#     """ Get game usage from API
#     * <param> string game_id
#     """
#     ret_val = None

#     params = {
#         'game_id' : game_id
#     }
    
#     # 1. Make request to API via cURL
#     usage_url = urljoin(base=AppConfig.APP_CONFIG['WEBSITE_API_URL_BASE'], url="getMonthlyGameUsage")
#     api_response = APIRequest(url=usage_url, request_type=RESTType.GET, params=params).Execute(current_app.logger)

#     # 2. Convert response to a GameUsage object
#     if api_response:
#         if api_response.Status == ResponseStatus.OK:
#             if api_response.Value:
#                 ret_val = GameUsage.FromDict(api_response.Value)
#             else:
#                 err_str = f"getGameUsage request, for game_id={game_id}, had empty value element!\nResponse message: {api_response.Message}"
#                 current_app.logger.error(err_str)
#         else:
#             err_str = f"getGameUsage request, for game_id={game_id}, was unsuccessful:\n{api_response.Message}"
#             current_app.logger.error(err_str)
#     else:
#         err_str = f"getGameUsage request, for game_id={game_id}, got no response object!"
#         current_app.logger.error(err_str)

#     return ret_val
