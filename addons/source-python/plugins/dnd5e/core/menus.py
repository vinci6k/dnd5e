# ../dnd5e/core/menus.py

# Source.Python
from menus import Text, SimpleOption, PagedOption
from menus.base import _translate_text
from listeners.tick import Delay


__all__ = (
    'BLANK_SPACE',
    'TextEx',
    'SimpleOptionEx',
    'PagedOptionEx'
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


class SimpleOptionEx(SimpleOption):
    """Extended SimpleOption class."""

    def __init__(
            self, choice_index, text, value=None,
            highlight=True, selectable=True):
        """Initializes the object."""
        super().__init__(choice_index, text, value, highlight, selectable)

        self.original_text = text
        self.disabled = False

    def disable(self, text=None, duration=0):
        """Disables the option and changes its appearance.

        Args:
            text (str): Replaces the option's original text.
            duration (float): Seconds until the option gets renabled.
        """
        # Is the option already disabled?
        if self.disabled:
            # Don't go further.
            return

        self.selectable = False
        self.highlight = False
        self.disabled = True

        if text is not None:
            self.text = text

        if duration > 0:
            Delay(duration, self.enable)

    def enable(self):
        """Enables the option and restores its appearance to normal."""
        if not self.disabled:
            return

        self.selectable = True
        self.highlight = True
        self.disabled = False
        self.text = self.original_text


class PagedOptionEx(PagedOption):
    """Extended PagedOption class.

    Args:
        text (str): The text that should be displayed.
        value: The value that should be passed to the menu's selection
            callback.
        highlight (bool): Set this to True if the text should be highlighted.
        selectable (bool): Set this to True if the option should be selectable.

    Attributes:
        highlight_in (bool): Should the text start with the highlight disabled
            and enable the highlight after a small delay?
    """
    tag = ''

    def __init__(self, text, value=None, highlight=True, selectable=True):
        """Initialize the object."""
        super().__init__(text, value, highlight, selectable)
        self.highlight_in = False

    def _render(self, player_index, choice_index):
        """Renders the data."""
        if self.highlight_in:
            self.highlight = False
            Delay(0.1, setattr, (self, 'highlight', True))
            self.highlight_in = False

        return '{0}{1}. {2} {3}\n'.format(
            self._get_highlight_prefix(),
            choice_index,
            _translate_text(self.text, player_index),
            _translate_text(self.tag, player_index)
        )
