# ../dnd5e/core/strings.py

# Source.Python
from paths import TRANSLATION_PATH
from translations.strings import LangStrings


__all__ = (
    'CHALLENGE_STRINGS',
    'MENU_STRINGS'
)


CHALLENGE_STRINGS = LangStrings(
    TRANSLATION_PATH / 'dnd5e' / 'challenge_strings')


MENU_STRINGS = LangStrings(TRANSLATION_PATH / 'dnd5e' / 'menu_strings')
