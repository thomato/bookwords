from bs4 import BeautifulSoup


def parse_html(html: str) -> str:
    """Extract text content from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()
