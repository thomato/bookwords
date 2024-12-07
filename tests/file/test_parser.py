from file import parse_html


def test_extract_text_from_simple_html():
    # Arrange
    html = "<p>Hello, world!</p>"

    # Act
    result = parse_html(html)

    # Assert
    assert result == "Hello, world!"


def test_extract_text_from_nested_html():
    # Arrange
    html = """
    <div>
        <h1>Title</h1>
        <p>First paragraph</p>
        <p>Second paragraph</p>
    </div>
    """

    # Act
    result = parse_html(html)

    # Assert
    expected = "Title\nFirst paragraph\nSecond paragraph"
    assert result.strip() == expected


def test_extract_text_from_html_with_attributes():
    # Arrange
    html = '<div class="content"><p id="main">Text with attributes</p></div>'

    # Act
    result = parse_html(html)

    # Assert
    assert result == "Text with attributes"


def test_extract_text_from_empty_html():
    # Arrange
    html = "<div></div>"

    # Act
    result = parse_html(html)

    # Assert
    assert result == ""


def test_extract_text_handles_special_characters():
    # Arrange
    html = "<p>&quot;Special &amp; characters&quot;</p>"

    # Act
    result = parse_html(html)

    # Assert
    assert result == '"Special & characters"'


def test_extract_text_with_invalid_html():
    # Arrange
    html = "<p>Unclosed paragraph"

    # Act
    result = parse_html(html)

    # Assert
    assert result == "Unclosed paragraph"


def test_extract_text_with_script_and_style_tags():
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
    result = parse_html(html)

    # Assert
    assert "Visible content" in result
    assert "console.log" not in result
    assert "color: red" not in result


def test_extract_text_preserves_newlines():
    # Arrange
    html = "<p>First line</p>\n<p>Second line</p>"

    # Act
    result = parse_html(html)

    # Assert
    assert "First line" in result
    assert "Second line" in result
