
class PipelineElement:
    def __init__(self, title:str, text:str, image, image_active, month:str, file_links, selector:str, is_active:bool, is_transition_button:bool):
        self._title = title
        self._text = text
        self._month = month
        self._file_links = file_links
        self._image = image
        self._image_active = image_active
        self._selector = selector
        self._is_active = is_active
        self._is_transition_button = is_transition_button

    @property
    def Title(self):
        return self._title
    @property
    def Text(self):
        return self._text
    @property
    def Image(self):
        return self._image
    @property
    def ActiveImage(self):
        return self._image_active
    @property
    def Month(self):
        return self._month
    @property
    def FileLinks(self):
        return self._file_links
    @property
    def Selector(self) -> str:
        return self._selector

    @property
    def Disabled(self) -> bool:
        return len(self.FileLinks) > 0
    @property
    def IsActive(self) -> bool:
        return self._is_active
    @property
    def IsTransition(self) -> bool:
        return self._is_transition_button

