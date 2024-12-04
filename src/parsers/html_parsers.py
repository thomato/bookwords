from abc import abstractmethod, ABC
from bs4 import BeautifulSoup


class HTMLParser(ABC):
    """Interface for parsing HTML content."""

    @abstractmethod
    def extract_text(self, html: str) -> str:
        pass


class BeautifulSoupHTMLParser(HTMLParser):
    def extract_text(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text()
