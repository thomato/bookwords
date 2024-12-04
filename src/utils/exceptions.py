from pathlib import Path
from typing import Optional


class BookProcessingError(Exception):
    """Exception raised when processing a book file fails."""

    def __init__(
        self,
        message: str,
        file_path: Optional[Path] = None,
        original_error: Optional[Exception] = None,
    ):
        self.file_path = file_path
        self.original_error = original_error
        self.message = message

        # Build detailed error message
        detailed_message = message
        if file_path:
            detailed_message += f" (File: {file_path})"
        if original_error:
            detailed_message += f" | Original error: {str(original_error)}"

        super().__init__(detailed_message)

    def __str__(self) -> str:
        """Return a string representation of the error."""
        return self.message
