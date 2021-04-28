# ../dnd5e/core/config.py

# Source.Python
from config.manager import ConfigManager

# D&D 5e
from ..info import info


__all__ = (
    'bot_races',
    'bot_classes'
    )


# Create a config file in the '../cfg/source-python/dnd5e' folder.
with ConfigManager(f'{info.name}/config.cfg', f'{info.name}_') as config:
    config.header = f'{info.verbose_name} Settings'

    bot_races = config.cvar(
        'bot_races', 'Human, Elf, Dwarf',
        'Which races are the bots allowed to play as?'
        )

    bot_classes = config.cvar(
        'bot_classes', 'Fighter',
        'Which classes are the bots allowed to play as?'
        )
