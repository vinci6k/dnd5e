# ../dnd5e/core/menus.py

# Source.Python
from menus import Text
from menus.base import _translate_text


__all__ = (
    'BLANK_SPACE',
    'TextEx'
)


BLANK_SPACE = ' '


class TextEx(Text):
    """Extended Text class."""

    empty_text = ' \n'

    def __init__(self, text, *other_texts):
        """Initializes the object."""
        super().__init__(text)

        # Store 'text' and all the other specified strings in a list.
        self.texts = [t for t in (text, *other_texts)]
        self.hidden = False
        self._text_index = 0

    def next_text(self):
        """Changes the text to the next one in line."""
        if self._text_index < len(self.texts) - 1:
            self._text_index += 1

        self.text = self.texts[self._text_index]

    def prev_text(self):
        """Changes the text to the previous one in line."""
        if self._text_index > 0:
            self._text_index -= 1

        self.text = self.texts[self._text_index]

    def _render(self, player_index, choice_index=None):
        """Renders the text, if it's not hidden."""
        if self.hidden:
            return TextEx.empty_text

        return str(_translate_text(self.text, player_index)) + '\n'
