import html
from typing import List

from models.Publication import Publication

class GameDetails:
    def __init__(self, game_id:str,  name:str,      description:str,
                 thumbnail_path:str, play_link:str, source_link:str,
                 developer_name:str, developer_link:str,
                 publications:List[Publication]):
        self._game_id          : str               = game_id
        self._game_name        : str               = name
        self._game_description : str               = description
        self._thumbnail_path   : str               = thumbnail_path
        self._play_link        : str               = play_link
        self._source_link      : str               = source_link
        self._developer_name   : str               = developer_name
        self._developer_link   : str               = developer_link
        self._publications     : List[Publication] = publications

    @staticmethod
    def FromJson(game_id, json) -> "GameDetails":
        # game object returned from api
        data = json.loads(json)
        
        return GameDetails.FromArray(game_id, data)

    @staticmethod
    def FromArray(game_id, data) -> "GameDetails":
        # build the array for publications
        publications = []
        for value in data.get('studies', []):
            publications.append(Publication.FromObj(value))

        return GameDetails(
            game_id=game_id,
            name=data.get('game_name'),
            description=data.get('game_description'),
            thumbnail_path=data.get('thumbnail_path'),
            play_link=data.get('play_link'),
            source_link=data.get('source_link'),
            developer_name=data.get('developers')[0].get('name'),
            developer_link=data.get('developers')[0].get('link'),
            publications=publications
        )

    # Properties
    @property
    def ID(self, html_safe:bool=True) -> str:
        return html.escape(self._game_id, quote=True) if html_safe else self._game_id
    @ID.setter
    def ID(self, game_id:str):
        self._game_id = game_id

    @property
    def Name(self, html_safe:bool=True) -> str:
        return html.escape(self._game_name, quote=True) if html_safe else self._game_name
    @Name.setter
    def Name(self, name:str):
        self._game_name = name
    
    @property
    def Description(self, html_safe:bool=True) -> str:
        return html.escape(self._game_description, quote=True) if html_safe else self._game_description
    @Description.setter
    def Description(self, description:str):
        self._game_description = description
    
    @property
    def PlayLink(self, html_safe:bool=True) -> str:
        return html.escape(self._play_link, quote=True) if html_safe else self._play_link
    @PlayLink.setter
    def PlayLink(self, link:str):
        self._play_link = link
    
    @property
    def SourceLink(self, html_safe:bool=True) -> str:
        return html.escape(self._source_link, quote=True) if html_safe else self._source_link
    @SourceLink.setter
    def SourceLink(self, link:str):
        self._source_link = link
    
    @property
    def ThumbPath(self, html_safe:bool=True) -> str:
        return html.escape(self._thumbnail_path, quote=True) if html_safe else self._thumbnail_path
    @ThumbPath.setter
    def ThumbPath(self, path:str):
        self._thumbnail_path = path
    
    @property
    def DeveloperName(self, html_safe:bool=True) -> str:
        return html.escape(self._developer_name, quote=True) if html_safe else self._developer_name
    @DeveloperName.setter
    def DeveloperName(self, name:str):
        self._developer_name = name
    
    @property
    def DeveloperLink(self, html_safe:bool=True) -> str:
        return html.escape(self._developer_link, quote=True) if html_safe else self._developer_link
    @DeveloperLink.setter
    def DeveloperLink(self, link:str):
        self._developer_link = link

    @property
    def Publications(self) -> List[Publication]:
        return self._publications

    @property
    def DeveloperIconFilename(self, html_safe:bool=True) -> str:
        path = None
        match self._developer_name:
            case 'PBS Wisconsin':
                path = 'pbs/pbs-64.png'
            case 'MIT Education Arcade':
                path = 'mit/mit-64.png'
            case _:
                path = 'fieldday/fieldday-64.png'
        return html.escape(path, quote=True) if html_safe else path

    # Set methods