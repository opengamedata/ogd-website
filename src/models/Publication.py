from typing import Any, Dict, List, Optional

class Publication:
    def __init__(self, name:Optional[str],   authors:Optional[List[str]], year:Optional[int],
                 published_in:Optional[str], paper_link:Optional[str],    project_code_link:Optional[str]):
        self._name              : Optional[str]       = name
        self._authors           : Optional[List[str]] = authors
        self._year              : Optional[int]       = year
        self._published_in      : Optional[str]       = published_in
        self._paper_link        : Optional[str]       = paper_link
        self._project_code_link : Optional[str]       = project_code_link

    @staticmethod
    def FromObj(obj:Dict[str, Any]):
        return Publication(
            name              = obj.get('name'),
            paper_link        = obj.get('paper_link'),
            authors           = obj.get('authors'),
            year              = obj.get('year'),
            project_code_link = obj.get('project_code_link'),
            published_in      = obj.get('published_in')
        )

    @property
    def Authors(self) -> Optional[List[str]]:
        return self._authors
    @property
    def Name(self) -> Optional[str]:
        return self._name
    @property
    def PaperLink(self) -> Optional[str]:
        return self._paper_link
    @property
    def FormattedPaperLink(self) -> Optional[str]:
        return f"<a href=\"{self.PaperLink}\" target=\"_blank\">{self.Name}.</a>" if self.PaperLink else f"{self.Name}."
    @property
    def Year(self) -> Optional[int]:
        return self._year
    @property
    def ProjectCodeLink(self) -> Optional[str]:
        return self._project_code_link
    @property
    def FormattedCodeLink(self) -> str:
        return f"<a class=\"btn btn-outline-secondary btn-publication mt-3\" href=\"{self.ProjectCodeLink}\" target=\"_blank\">View Project Code</a>" if self._project_code_link else "<span>(Project Code Not Available)</span>"
    @property
    def PublishedIn(self) -> Optional[str]:
        return self._published_in
    @property
    def FormattedPublication(self) -> str:
        return f"{', '.join(self.Authors or [])}. ({self.Year}). {self.FormattedPaperLink} {self.PublishedIn}. <br>{self.FormattedCodeLink}"
