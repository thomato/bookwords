from src.file.parsers import BeautifulSoupHTMLParser


class TestBeautifulSoupHTMLParser:
    def setup_method(self):
        self.parser = BeautifulSoupHTMLParser()

    def test_extract_text_from_simple_html(self):
        # Arrange
        html = "<p>Hello, world!</p>"

        # Act
        result = self.parser.extract_text(html)

        # Assert
        assert result == "Hello, world!"

    def test_extract_text_from_nested_html(self):
        # Arrange
        html = """
        <div>
            <h1>Title</h1>
            <p>First paragraph</p>
            <p>Second paragraph</p>
        </div>
        """

        # Act
        result = self.parser.extract_text(html)

        # Assert
        expected = "Title\nFirst paragraph\nSecond paragraph"
        assert result.strip() == expected

    def test_extract_text_from_html_with_attributes(self):
        # Arrange
        html = (
            '<div class="content"><p id="main">Text with attributes</p></div>'
        )

        # Act
        result = self.parser.extract_text(html)

        # Assert
        assert result == "Text with attributes"

    def test_extract_text_from_empty_html(self):
        # Arrange
        html = "<div></div>"

        # Act
        result = self.parser.extract_text(html)

        # Assert
        assert result == ""

    def test_extract_text_handles_special_characters(self):
        # Arrange
        html = "<p>&quot;Special &amp; characters&quot;</p>"

        # Act
        result = self.parser.extract_text(html)

        # Assert
        assert result == '"Special & characters"'

    def test_extract_text_with_invalid_html(self):
        # Arrange
        html = "<p>Unclosed paragraph"

        # Act
        result = self.parser.extract_text(html)

        # Assert
        assert result == "Unclosed paragraph"

    def test_extract_text_with_script_and_style_tags(self):
        # Arrange
        html = """
        <html>
            <head>
                <style>
                    body { color: red; }
                </style>
            </head>
            <body>
                <script>
                    console.log('Hello');
                </script>
                <p>Visible content</p>
            </body>
        </html>
        """

        # Act
        result = self.parser.extract_text(html)

        # Assert
        assert "Visible content" in result
        assert "console.log" not in result
        assert "color: red" not in result

    def test_extract_text_preserves_newlines(self):
        # Arrange
        html = "<p>First line</p>\n<p>Second line</p>"

        # Act
        result = self.parser.extract_text(html)

        # Assert
        assert "First line" in result
        assert "Second line" in result
