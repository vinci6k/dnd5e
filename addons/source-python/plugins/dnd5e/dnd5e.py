from messages import SayText2
from messages import HudMsg
from pprint import pprint
from events import Event
from events.hooks import PreEvent
from players import PlayerGenerator
from players.helpers import userid_from_index
from players.helpers import index_from_userid
from players.helpers import uniqueid_from_index
from players.helpers import userid_from_edict
from players.constants import PlayerButtons
from players.entity import Player
from players.dictionary import PlayerDictionary
from entities.entity import Entity
from entities.entity import BaseEntity
from entities.hooks import EntityCondition
from entities.hooks import EntityPreHook
from entities.constants import DamageTypes
from entities.constants import RenderMode
from entities.constants import RenderEffects
from entities import TakeDamageInfo
from entities import CheckTransmitInfo
from entities.helpers import index_from_basehandle
from entities.helpers import index_from_edict
from entities.helpers import index_from_inthandle
from entities.helpers import index_from_pointer
from mathlib import Vector
from mathlib import NULL_VECTOR
from mathlib import QAngle
from filters.entities import EntityIter
from filters.players import PlayerIter
from filters.recipients import RecipientFilter
from memory import make_object
from memory.hooks import PreHook
from os.path import join, dirname, abspath
from listeners import OnPlayerRunCommand
from listeners.tick import Delay
from listeners.tick import GameThread
from weapons.dictionary import WeaponDictionary
from weapons.entity import Weapon
from weapons.manager import weapon_manager
from engines.server import engine_server
from engines.server import global_vars
from effects.base import TempEntity
from colors import Color
from plugins.manager import plugin_manager
from menus import SimpleMenu
from menus import Text
from menus import PagedMenu
from menus import PagedOption
from commands.say import SayFilter
from commands.say import SayCommand
from commands.client import ClientCommand
from commands import CommandReturn
from itertools import chain 
from engines.precache import Model
from engines.sound import Sound
from engines.trace import engine_trace
from engines.trace import ContentMasks
from engines.trace import GameTrace
from engines.trace import Ray
from engines.trace import TraceFilterSimple
from stringtables import string_tables
from memory import NULL
import math
import random
import os
import sys
import shutil
import json
import time
import datetime
import traceback
import requests

try:
    # Is Floating Damage Numbers installed on this server?
    from fdn.core.colors import WHITE
    from fdn.core.constants import DISTANCE_MULTIPLIER
    from fdn.core.floating_number import FloatingNumber
    from fdn.core.players import PlayerFDN
except ImportError:
    # Nope.
    FloatingNumber = None


database = {}
databaseLocation = join(dirname(__file__), "dnd5e.db")
restfulFile = join(dirname(__file__), "restfulURL.txt")
bugFile = join(dirname(__file__), 'bugreports.txt')
webDatabase = ''
sourceFiles = ''
release = ''
debugValue = True
restfulURL = None
###############################################################
# XP Values
killXP = 10
knifeXP = killXP*2
killSpreeXP = 5
assistXP = 3
finishXP = 7
headshotXP = 14
plantBombXP = 25
defuseBombXP = 50
explodedBombXP = 25
roundWinXP = 50
rescueXP = 10
humanXP = 1.1
higherLevelXP = 2

xpDuringWarmup = False # Set to true to allow earning Xp during warmup
###############################################################
cterrorists = 2
terrorists = 3
###############################################################

sounds = {  'fire':'weapons/molotov/fire_ignite_1.wav',
            'taser':'weapons/taser/taser_hit.wav',
            'flashbang':'weapons/flashbang/flashbang_explode2.wav',
            'levelup':'ui/xp_levelup.wav',
            'heal':'items/medshot4.wav',
            'knife':'weapons/knife/knife_hit2.wav',
            'wound':'physics/flesh/flesh_impact_bullet5.wav',
            'medkit':'items/medcharge4.wav',
            'water':'player/water/pl_wade2.wav',
            'bomb':'weapons/c4/c4_exp_deb1.wav',
            'rocks':'physics/destruction/smash_rockcollapse1.wav',
            'chicken':'ambient/creatures/chicken_panic_03.wav',
            'steam':'ambient/machines/steam_release_2.wav'
        }


###############################################################


player_models = {
    # Terrorists
    2: [
        # Anarchist
        ('tm_anarchist.mdl', 't_arms_anarchist.mdl'),
        ('tm_anarchist_varianta.mdl', 't_arms_anarchist.mdl'),
        ('tm_anarchist_variantb.mdl', 't_arms_anarchist.mdl'),
        ('tm_anarchist_variantc.mdl', 't_arms_anarchist.mdl'),
        ('tm_anarchist_variantd.mdl', 't_arms_anarchist.mdl'),
        # Pirate
        ('tm_pirate.mdl', 't_arms_pirate.mdl'),
        ('tm_pirate_varianta.mdl', 't_arms_pirate.mdl'),
        ('tm_pirate_variantb.mdl', 't_arms_pirate.mdl'),
        ('tm_pirate_variantc.mdl', 't_arms_pirate.mdl'),
        ('tm_pirate_variantd.mdl', 't_arms_pirate.mdl'),
        # Professional
        ('tm_professional.mdl', 't_arms_professional.mdl'),
        ('tm_professional_var1.mdl', 't_arms_professional.mdl'),
        ('tm_professional_var2.mdl', 't_arms_professional.mdl'),
        ('tm_professional_var3.mdl', 't_arms_professional.mdl'),
        ('tm_professional_var4.mdl', 't_arms_professional.mdl'),
        # Separatist
        ('tm_separatist.mdl', 't_arms_separatist.mdl'),
        ('tm_separatist_varianta.mdl', 't_arms_separatist.mdl'),
        ('tm_separatist_variantb.mdl', 't_arms_separatist.mdl'),
        ('tm_separatist_variantc.mdl', 't_arms_separatist.mdl'),
        ('tm_separatist_variantd.mdl', 't_arms_separatist.mdl'),
        # Balkan
        ('tm_balkan_varianta.mdl', 't_arms_balkan.mdl'),
        ('tm_balkan_variantb.mdl', 't_arms_balkan.mdl'),
        ('tm_balkan_variantc.mdl', 't_arms_balkan.mdl'),
        ('tm_balkan_variantd.mdl', 't_arms_balkan.mdl'),
        ('tm_balkan_variante.mdl', 't_arms_balkan.mdl'),
        # Leet
        ('tm_leet_varianta.mdl', 't_arms_leet.mdl'),
        ('tm_leet_variantb.mdl', 't_arms_leet.mdl'),
        ('tm_leet_variantc.mdl', 't_arms_leet.mdl'),
        ('tm_leet_variantd.mdl', 't_arms_leet.mdl'),
        ('tm_leet_variante.mdl', 't_arms_leet.mdl'),
        # Phoenix
        ('tm_phoenix.mdl', 't_arms_phoenix.mdl'),
        ('tm_phoenix_varianta.mdl', 't_arms_phoenix.mdl'),
        ('tm_phoenix_variantb.mdl', 't_arms_phoenix.mdl'),
        ('tm_phoenix_variantc.mdl', 't_arms_phoenix.mdl'),
        ('tm_phoenix_variantd.mdl', 't_arms_phoenix.mdl'),
    ],
    # Counter-Terrorists
    3: [
        # GIGN
        ('ctm_gign.mdl', 'ct_arms_gign.mdl'),
        ('ctm_gign_varianta.mdl', 'ct_arms_gign.mdl'),
        ('ctm_gign_variantb.mdl', 'ct_arms_gign.mdl'),
        ('ctm_gign_variantc.mdl', 'ct_arms_gign.mdl'),
        ('ctm_gign_variantd.mdl', 'ct_arms_gign.mdl'),
        # GSG-9
        ('ctm_gsg9.mdl', 'ct_arms_gsg9.mdl'),
        ('ctm_gsg9_varianta.mdl', 'ct_arms_gsg9.mdl'),
        ('ctm_gsg9_variantb.mdl', 'ct_arms_gsg9.mdl'),
        ('ctm_gsg9_variantc.mdl', 'ct_arms_gsg9.mdl'),
        ('ctm_gsg9_variantd.mdl', 'ct_arms_gsg9.mdl'),
        # ST-6
        ('ctm_st6.mdl', 'ct_arms_st6.mdl'),
        ('ctm_st6_varianta.mdl', 'ct_arms_st6.mdl'),
        ('ctm_st6_variantb.mdl', 'ct_arms_st6.mdl'),
        ('ctm_st6_variantc.mdl', 'ct_arms_st6.mdl'),
        ('ctm_st6_variantd.mdl', 'ct_arms_st6.mdl'),
        # FBI
        ('ctm_fbi.mdl', 'ct_arms_fbi.mdl'),
        ('ctm_fbi_varianta.mdl', 'ct_arms_fbi.mdl'),
        ('ctm_fbi_variantb.mdl', 'ct_arms_fbi.mdl'),
        ('ctm_fbi_variantc.mdl', 'ct_arms_fbi.mdl'),
        ('ctm_fbi_variantd.mdl', 'ct_arms_fbi.mdl'),
        # IDF
        ('ctm_idf.mdl', 'ct_arms_idf.mdl'),
        ('ctm_idf_variantb.mdl', 'ct_arms_idf.mdl'),
        ('ctm_idf_variantc.mdl', 'ct_arms_idf.mdl'),
        ('ctm_idf_variantd.mdl', 'ct_arms_idf.mdl'),
        ('ctm_idf_variante.mdl', 'ct_arms_idf.mdl'),
        ('ctm_idf_variantf.mdl', 'ct_arms_idf.mdl'),
        # SAS
        ('ctm_sas.mdl', 'ct_arms_sas.mdl'),
        ('ctm_sas_varianta.mdl', 'ct_arms_sas.mdl'),
        ('ctm_sas_variantb.mdl', 'ct_arms_sas.mdl'),
        ('ctm_sas_variantc.mdl', 'ct_arms_sas.mdl'),
        ('ctm_sas_variantd.mdl', 'ct_arms_sas.mdl'),
        ('ctm_sas_variante.mdl', 'ct_arms_sas.mdl'),
        # SWAT
        ('ctm_swat.mdl', 'ct_arms_swat.mdl'),
        ('ctm_swat_varianta.mdl', 'ct_arms_swat.mdl'),
        ('ctm_swat_variantb.mdl', 'ct_arms_swat.mdl'),
        ('ctm_swat_variantc.mdl', 'ct_arms_swat.mdl'),
        ('ctm_swat_variantd.mdl', 'ct_arms_swat.mdl'),
    ]
}


# Create a list of all the player models (used for Confusion).
_all_player_models = player_models[2] + player_models[3]


# Dictionary used to determine which weapon the player is trying to buy within
# the 'buy_internal' hook. NOTE: This can lead to false positives, seeing as
# some weapons share the same slot. It works fine in D&D 5e because of the way
# weapons (and weapon restrictions) are grouped together.
weapon_buymenu_slots = {
    # Pistol
    **dict.fromkeys(('glock', 'hkp2000', 'usp_silencer'), 2),
    'elite': 3,
    'p250': 4,
    **dict.fromkeys(('tec9', 'fiveseven', 'cz75a'), 5),
    **dict.fromkeys(('deagle', 'revolver'), 6),
    # SMG
    'mac10': 8,
    'mp9': 8,
    **dict.fromkeys(('mp7', 'mp5sd'), 9),
    'ump': 10,
    'p90': 11,
    'bizon': 12,
    # Rifle
    **dict.fromkeys(('galil', 'famas'), 14),
    **dict.fromkeys(('ak47', 'm4a1', 'm4a1_silencer'), 15),
    'ssg08': 16,
    **dict.fromkeys(('sg556', 'aug'), 17),
    'awp': 18,
    **dict.fromkeys(('g3sg1', 'scar20'), 19),
    # Heavy
    'nova': 20,
    'xm1014': 21,
    **dict.fromkeys(('sawedoff', 'mag7'), 22),
    'm249': 23,
    'negev': 24,
    # Grenade
    **dict.fromkeys(('molotov', 'incgrenade'), 26),
    'decoy': 27,
    'flashbang': 28,
    'hegrenade': 29,
    'smokegrenade': 30,
    # Equipment
    'taser': 34
}


# Sound used when a player tries to buy a restricted weapon.
CANT_BUY_SOUND = Sound('ui/weapon_cant_buy.wav')


knife = {'knife', 'c4'}
pistols = {'glock', 'elite', 'p250', 'tec9', 'cz75a', 'deagle', 'revolver', 'usp_silencer', 'hkp2000', 'fiveseven'}
heavypistols = {'deagle', 'revolver'}
taser = {'taser'}
shotguns = {'nova', 'xm1014', 'sawedoff', 'mag7'}
lmg = {'m249', 'negev'}
smg = {'mac10', 'mp7', 'ump45', 'p90', 'bizon', 'mp9'}
rifles = {'galilar', 'ak47', 'ssg08', 'sg556', 'famas', 'm4a1', 'm4a1_silencer', 'aug'}
bigsnipers = {'awp', 'g3sg1', 'scar20'}
grenades = {'molotov', 'decoy', 'flashbang', 'hegrenade', 'smokegrenade', 'incgrenade'}
allWeapons = list(chain(knife, pistols, heavypistols, taser, shotguns, lmg, smg, rifles, bigsnipers, grenades))


class DateTimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()

        return super(DateTimeEncoder, self).default(obj)

def dice(number, sides):
    total = 0
    for die in range(1,number+1):
        total += random.randint(1,sides)
    return total

def diceCheck(check, player, attacker):
    #Check should be a tuple of (Int, Str)
    #                           Save, Type
    
    bonus = 0
    if hasattr(player, 'bless'):
        if player.bless:
            bonus += dice(1,4)
            
    dc = check[0]
    save = check[1]
    rolledAdvantage = False
    
    result = dice(1,20) + bonus + (player.getProficiencyBonus() if save in player.getSaves() else 0)
    if result < dc:
        
        if hasattr(player, 'indomitable'):  # or (check[1] == 'Dexterity' and player.getClass() == rogue.name and player.getLevel() >= 5) or (player.getRace() == gnome.name and save in ['Intelligence', 'Charisma', 'Wisdom']):
            if player.indomitable > 1:
                player.indomitable -= 1
                result = dice(1,20) + bonus + (player.getProficiencyBonus() if save in player.getSaves() else 0)
                if result >= dc:
                    messagePlayer('Your Indomitable nature saved you from a nasty effect!')
                    rolledAdvantage = True
        
        if save == 'Dexterity' and player.getClass() == rogue.name and player.getLevel() >= 5:
            result = dice(1,20) + bonus + (player.getProficiencyBonus() if save in player.getSaves() else 0)
            if result >= dc:
                messagePlayer('Your Evasive trait saved you from a nasty effect!')
                rolledAdvantage = True
                
        if not rolledAdvantage and player.getRace() == gnome.name:
            if save in ['Intelligence', 'Charisma', 'Wisdom']:
                result = dice(1,20) + bonus + (player.getProficiencyBonus() if save in player.getSaves() else 0)
                if result >= dc:
                    messagePlayer('Your Gnomish cunning saved you from a nasty effect!')
                    rolledAdvantage = True
                    
    return result >= dc


class DNDClass():
    
    classes = []
    defaultClass = None
    
    def __init__(self, name, description=None, requiredClasses=None, defaultClass=False, saves=[], weapons=[]):
            
        self.name = name
        #self.requiredClasses = {fighter: 3, cleric: 3}
        self.requiredClasses = requiredClasses
        self.description = description
        self.saves = saves
        self.weapons = weapons
        DNDClass.classes.append(self)
        if defaultClass:
            if not DNDClass.defaultClass:
                DNDClass.defaultClass = self

cleric = DNDClass('Cleric', 'A priest who follows a path of good or evil. Uses divine power to fight.', saves=['Wisdom'])       
cleric.weapons = list(chain(knife, pistols, heavypistols, taser, shotguns, lmg, smg))
cleric.weaponDesc = ['Pistols', 'Heavy Pistols', 'Taser', 'Shotguns', 'LMGs', 'SMGs']

fighter = DNDClass('Fighter', 'Uses martial prowess and tactical maneuvers to defeat enemies.', defaultClass=True, saves=['Fortitude'])
fighter.weapons = list(chain(knife, pistols, heavypistols, shotguns, lmg, smg, rifles, bigsnipers, {'hegrenade'}))
fighter.weaponDesc = ['HE Grenade', 'Pistols', 'Heavy Pistols', 'Shotguns', 'LMGs', 'SMGs', 'Rifles', 'AWP', 'Autosnipers']

rogue = DNDClass('Rogue', 'Strikes from the shadows and uses guile to outmaneuver enemies.', saves=['Dexterity'])
rogue.weapons = list(chain(knife, pistols, heavypistols, shotguns, smg, {'ssg08'}, grenades))
rogue.weaponDesc = ['Pistols', 'Heavy Pistols', 'Shotguns', 'SMGs', 'Scout', 'Grenades', 'Taser']

sorcerer = DNDClass('Sorcerer', 'Descended from a magical blood line, their magic is innate and awe-inspiring.', saves=['Constitution'])
sorcerer.weapons = list(chain(knife, pistols, grenades))
sorcerer.weaponDesc = ['Pistols', 'Grenades', 'Taser']

monk = DNDClass('Monk', 'Disciplined. Quick. Mind and body. A master of both.', requiredClasses={fighter:7, rogue:7}, saves=['Strength', 'Dexterity'])
monk.weapons = list(chain(knife, pistols, heavypistols, smg))
monk.weaponDesc = ['Pistols', 'Heavy Pistols', 'SMGs']

paladin = DNDClass('Paladin', 'A holy crusader who has taken an oath to serve a higher calling.', requiredClasses={fighter:7,cleric:7}, saves=['Wisdom', 'Charisma'])
paladin.weapons = list(chain(knife, pistols, heavypistols, shotguns, lmg, smg, rifles, bigsnipers, {'hegrenade'}))
paladin.weaponDesc = ['HE Grenade', 'Pistols', 'Heavy Pistols', 'Shotguns', 'LMGs', 'SMGs', 'Rifles', 'AWP', 'Autosnipers']

warlock = DNDClass('Warlock', 'A Witch/Warlock serves a greater patron for a chance at greater power.', requiredClasses={cleric:7, sorcerer:7}, saves=['Wisdom', 'Charisma'])
warlock.weapons = list(chain(knife, pistols, grenades))
warlock.weaponDesc = ['Pistols', 'Grenades', 'Taser']

bard = DNDClass('Bard', 'Bards sing songs of encouragement to help their allies and hinder their enemies.', requiredClasses ={cleric:7, rogue:7}, saves=['Dexterity', 'Charisma'])
bard.weapons = list(chain(knife, pistols, heavypistols, shotguns, smg, {'ssg08'}, grenades))
bard.weaponDesc = ['Pistols', 'Heavy Pistols', 'Shotguns', 'SMGs', 'Scout', 'Grenades', 'Taser']

ranger = DNDClass('Ranger', 'Rangers master the wilderness, hunting foes of their choosing.', requiredClasses={rogue:7, fighter:7}, saves=['Dexterity', 'Strength'])
ranger.weapons = list(chain(knife, pistols, heavypistols, shotguns, smg, {'ssg08'}, grenades))
ranger.weaponDesc = ['Pistols', 'Heavy Pistols', 'Shotguns', 'SMGs', 'Scout', 'Grenades', 'Taser']

druid = DNDClass('Druid')
barbarian = DNDClass('Barbarian')


class Race():

    races = []
    defaultRace = None

    def __init__(self, name, description=None, levelAdjustment=0, defaultRace=False, weapons=[],saves=[]):
        self.name = name
        self.weapons = weapons
        self.description = description
        levelAdjustment = levelAdjustment
        self.saves = saves
        if defaultRace:
            if not Race.defaultRace:
                Race.defaultRace = self
        Race.races.append(self)


human = Race('Human', 'Humans excel at learning and gain bonus XP', defaultRace = True)
elf = Race('Elf', 'Elves are graceful and trained in many weapons (Can always use M4/AK/Scout)')
elf.weapons = list(chain({'m4a1', 'm4a1_silenced', 'ak47', 'ssg08'}))
elf.weaponDesc = ['M4', 'AK-47', 'Scout']
halfling = Race('Halfling', 'Halflings are short and nimble making them hard to see (Stealth faster, 10% Chance to Dodge)')
dwarf = Race('Dwarf', 'Dwarves have a strong stomach and strong back from years of drinking and mining (Use AWP, 25HP)')
dwarf.weapons = ['awp']
dwarf.weaponDesc = ['AWP']
dragonborn = Race('Dragonborn', 'Humanoid dragons that can breath fire upon their enemies (!cast Breath Weapon 3d8, Con halves)')
gnome = Race('Gnome', 'Gnomes are clever inventors and engineers (Can always use grenades, advantage on Int/Wis/Cha saves)')
#gnome.saves = ['Intelligence', 'Wisdom', 'Charisma'] Advantage is a special case
gnome.weapons = grenades
gnome.weaponDesc = ['Grenades']
halfelf = Race('Half-Elf', 'Half-Elves make charming diplomats (5% Bonus XP and 10% Damage Reduction')
halforc = Race('Half-Orc', "Half-Orcs aren't nearly as brutish as full-bloods, but nearly as strong (15% Damage)")
tiefling = Race('Tiefling', 'Tieflings blood have been tainted with infernal ancestry. Immune to flashes. (!cast Darkness - Blinds everyone near you)')

def error(message):
    print("\n\n------------------")
    print(message)
    print("------------------\n\n")        

class RPGPlayer(Player):

    def __init__(self, index):
        super().__init__(index)
        self.weaponFired = None
        self.hits = 0    
        self.stats = {}
        self.spellCooldown = 0
        self.toggleDelay = 0
        self.crit = False
        self.saves = []
        self.spell_names = []
        self.spellbook = None
        self.controllingbot = False
        self.queuedrace = None
        self.queuedclass = None
        # Used to prevent the player from picking up restricted weapons.
        self.weapon_restrictions = set()
        # Used to prevent the player from buying restricted weapons.
        self.buymenu_restrictions = set()
        # Should we update weapon restrictions for this player?
        self.new_restrictions = True

        if getSteamid(self.userid) in database:
            self.stats = database[getSteamid(self.userid)]
        else:
            messageServer("Welcome the new player, %s!"%self.name)
            self.setClass(DNDClass.defaultClass.name)
            self.stats['Gold'] = 0
            database[getSteamid(self.userid)] = self.stats

        self.setDefaults()    
        
    def setDefaults(self):
        for cls in DNDClass.classes:
            if cls.name not in self.stats:
                self.stats[cls.name] = {}
                self.stats[cls.name]['Level'] = 1
                self.stats[cls.name]['XP'] = 0
        self.stats['Last Played'] = time.time()
        self.stats['name'] = self.name
                
    def giveXP(self, xp, reason=None):
        global database
        self.setDefaults()
        
        if not MATCH_STARTED:
            if not xpDuringWarmup:
                messagePlayer('XP is set to only be earned when a match starts', self.index)
                return
                
        if self.controllingbot:
            if reason != 'winning the round!':
                messagePlayer('XP can not be earned while controlling a bot', self.index)
                return
        
        self.stats[self.getClass()]['XP'] += xp
        message = "\x06You have earned %s XP"%xp
        if reason:
            message += " for %s!"%reason
        else:
            message += "!"            
        messagePlayer(message, self.index)
        
        if self.getRace() == human.name:
            bonusXP = max(1, int(xp * humanXP - xp))
            self.stats[self.getClass()]['XP'] += bonusXP
            messagePlayer("\x06You have earned %s XP for being a Human"%bonusXP, self.index)
            
        if self.getRace() == halfelf.name:
            bonusXP = max(1, int(xp * ((humanXP - 1) / 2 + 1) - xp))
            self.stats[self.getClass()]['XP'] += bonusXP
            messagePlayer("\x06You have earned %s XP for being a Half-Elf"%bonusXP, self.index)
        
        if self.getLevel() < 20:
            xpNeeded = self.getLevel() * 1000
            while self.getXP() >= xpNeeded:
                xpNeeded = self.getLevel() * 1000
                playSound('ui/xp_levelup.wav', player=self)
                self.stats[self.getClass()]['Level'] += 1
                self.stats[self.getClass()]['XP'] -= xpNeeded
                messageServer('\x04Congratulations, %s! They are now Level %s!'%(self.name, self.getLevel()))
                if self.getLevel() >= 20:
                    break
        
        database[getSteamid(self.userid)] = self.stats        
            
    def getClass(self):
        return self.stats['Class']
        
    def setClass(self, dndClass):
    
        cls = None
        if dndClass in DNDClass.classes:
            cls = dndClass
        for c in DNDClass.classes:
            if dndClass == c.name:
                cls = c
        
        if not cls:
            error("%s IS NOT A VALID CLASS"%dndClass.name)
            return
        
        if self.meetsClassRequirements(cls):
            self.stats['Class'] = cls.name
            messagePlayer('You are now a %s'%cls.name, self.index)
            for save in cls.saves:
                self.saves.append(save)
            #necessary for new players
            if 'Race' in self.stats.keys():
                self.setRace(self.getRace(), False)
            else:
                self.setRace(Race.defaultRace.name)
        else:
            messagePlayer("You haven't unlocked that class yet", self.index)
        
        
    def getRace(self):
        return self.stats['Race']
        
    def setRace(self, race, message=True):
        
        r = None
        if race in Race.races:
            r = race
        for rc in Race.races:
            if race == rc.name:
                r = rc
                
        if not r:
            error("%S IS NOT A VALID RACE"%race)
        
        self.stats['Race'] = r.name
        if message:
            messagePlayer('You are now a %s'%r.name, self.index)
        for save in r.saves:
            self.save.append(save)                
            
    def getLevel(self, dndClass=None):
    
        if not dndClass:
            dndClass = self.getClass()
        
        if dndClass in DNDClass.classes:
            return self.stats[dndClass.name]['Level']
        
        for cls in DNDClass.classes:
            if cls.name == dndClass:
                return self.stats[dndClass]['Level']
        
        error("%s IS NOT A CLASS"%dndClass)
        
    def getXP(self, dndClass=None):
    
        if not dndClass:
            dndClass=  self.getClass()
        
        if dndClass in DNDClass.classes:
            return self.stats[dndClass.name]['XP']
        
        for cls in DNDClass.classes:
            if cls.name == dndClass:
                return self.stats[dndClass]['XP']
        
        error("%s IS NOT A CLASS"%dndClass)
        
    def meetsClassRequirements(self, cls):
        
        if not cls.requiredClasses:
            return True
        for c,l in cls.requiredClasses.items():
            if not self.getLevel(c.name) >= l:
                return False
        return True    
        
    def canUseWeapon(self, weapon):
    
        cls = None
        for c in DNDClass.classes:
            if self.getClass() == c.name:
                cls = c
                break
        if weapon in cls.weapons:
            return True
        
        race = None
        for r in Race.races:
            if self.getRace() == r.name:
                race = r
        if weapon in race.weapons:
            return True
        
        return False
        
    def getProficiencyBonus(self):
        return int((self.getLevel() - 1) / 4)
        
    def getSaves(self):
    
        return self.saves
                
    def heal(self, amount):
        if self.health != self.maxhealth:
            healed = self.health
            self.health = min(self.maxhealth, self.health + amount)
            healed = self.health - healed
            playSound('items/medshot4.wav', player=self)
            return healed
        return 0
        
    def resetBuffs(self):
        self.buff = False
        self.curse = False
        
    def stealthed(self):
        if self.dead:
            return False
        if not self.getClass() == rogue.name:
            return False
            
        if not hasattr(self, 'stealth'):
            self.stealth = time.time()
        return time.time() - self.stealth > (6.225 - (4.5/20)*self.getLevel() - (1 if self.getRace() == halfling.name else 0))
        
    def postStats(self):
        if not self.is_bot():
            if restfulURL:         
                
                for cls in DNDClass.classes:
                    data = {'action':'updatestats',
                        'value' : {
                          'steamid':getSteamid(self.userid),
                          'name':self.name,
                          'last_played':datetime.datetime.fromtimestamp(time.time()),
                          'classname':cls.name,
                          'level':self.stats[cls.name]['Level'],
                          'xp':self.stats[cls.name]['XP']
                            }
                        }

                    resp = requests.post(restfulURL, data=json.dumps(data, cls=DateTimeEncoder), headers={'Content-Type': 'application/json'})
                    if resp.status_code not in range(200,300):
                        error("UNCAUGHT REQUEST ERROR - %s %s\n%s"%(getSteamid(self.userid), self.name, resp.status_code))
                        return
                    
            
    def requestStats(self):
        if not self.is_bot():
            if restfulURL:
                messagePlayer('Retrieving your stats from online', self.index)
                data = {'action':'getstats',
                    'value':getSteamid(self.userid) 
                    } 
                resp = requests.post(restfulURL, data=json.dumps(data, cls=DateTimeEncoder), headers={'Content-Type': 'application/json'})        
                if resp.status_code not in range(200,300):
                    error("UNCAUGHT REQUEST ERROR - %s %s\n%s"%(getSteamid(self.userid), self.name, resp.status_code))
                    return
                if not 'server' in resp.text:
                    playerStats = json.loads(resp.text)
                    self.stats[self.getClass()]['Level'] = playerStats[self.getClass()]['Level']
                    self.stats[self.getClass()]['XP'] = playerStats[self.getClass()]['XP']
    
    @property
    def max_mana(self):
        """Returns the player's maximum mana."""
        level = self.getLevel()
        return int(level / 2) * 15 + (5 + 10 if level % 2 else 0)

    def change_model(self, model_name, arms_name):
        """Changes the player's world and arms model."""
        self.model = Model(f'models/player/custom_player/legacy/{model_name}')
        arms_path = f'models/weapons/{arms_name}'
        # Make sure the arms model is precached, otherwise the
        # player will have invisible arms.
        engine_server.precache_model(arms_path)
        # Change the player's arm model.
        self.set_property_string('m_szArmsModel', arms_path)

    def get_valid_targets(self):
        """Returns a list of players from the enemy team that are alive."""
        return list(PlayerIter(('alive', ['ct', 't'][self.team - 2])))

    def get_teammates(self):
        """Returns a list of players from the same team that are alive."""
        index = self.index
        teammates = []

        for player in PlayerIter(('alive', ['t', 'ct'][self.team - 2])):
            # Don't add the player looking for teammates as a teammate.
            if player.index == index:
                continue

            teammates.append(player)

        return teammates

    @property
    def restricted_weapons(self):
        """Returns a set of weapons that the player can't use."""
        class_name = self.getClass()
        race_name = self.getRace()
        allowed_weapons = []
        
        for dnd_class in DNDClass.classes:
            if class_name == dnd_class.name:
                allowed_weapons.extend(dnd_class.weapons)
                break

        for race in Race.races:
            if race_name == race.name:
                allowed_weapons.extend(race.weapons)
                break

        return set(allWeapons)^set(allowed_weapons)

    def update_weapon_restrictions(self):
        """Restricts weapons according to the player's race and class."""
        if not self.new_restrictions:
            return

        # Get rid of old restrictions.
        self.weapon_restrictions.clear()
        self.buymenu_restrictions.clear()

        restricted_weapons = self.restricted_weapons
        # Go through all the restricted weapons.
        for weapon_name in restricted_weapons:
            try:
                # Get the buymenu slot that this weapon occupies.
                slot = weapon_buymenu_slots[weapon_name]
            except KeyError:
                # Missing slot, skip this one.
                continue
            
            # Add it to the set, so the player can't buy this weapon.
            self.buymenu_restrictions.add(slot)

        # Block the player from picking up these weapons.
        self.weapon_restrictions.update(restricted_weapons)
        self.new_restrictions = False


players = PlayerDictionary(RPGPlayer)


def formatLine(line, menu, index=None):
    line = line.split(' ')
    
    if index is not None:
        player = players[index]
        spell_name = ' '.join(line[1:line.index('-')])

        if spell_name not in player.spell_names:
            # Add the name of the spell to the list.
            player.spell_names.append(spell_name)

    desc = ''
    i = 0
    while line:
        if len(desc) < 23:
            desc += line[i] + " "
        if len(desc) < 23:
            del(line[0])
            if not line:
                menu.append(desc)
        else:            
            desc = desc[0: len(desc) - len(line[0]) - 1]
            menu.append(desc)
            desc = ''

def createConfirmationMenu(obj, index):

    def confirmationMenuSelect(menu, index, choice):
        player = players[index]
        if choice.value:
            if player.dead:
                if choice.value in Race.races:
                    player.setRace(choice.value)
                if choice.value in DNDClass.classes:
                    player.setClass(choice.value)
            else:
                if choice.value in Race.races:
                    player.queuedrace = choice.value
                if choice.value in DNDClass.classes:
                    if player.meetsClassRequirements(choice.value):
                        player.queuedclass = choice.value
                    else:
                        messagePlayer("You haven't unlocked %s"%choice.value.name, index)
                        return
                msg = "You will spawn as a %s %s"%((player.queuedrace.name if player.queuedrace else player.getRace(), player.queuedclass.name if player.queuedclass else player.getClass()))
                messagePlayer(msg, index)

    confirmationMenu = PagedMenu(title="Play a %s?"%obj.name)
    confirmationMenu.append(PagedOption("Yes", obj))
    confirmationMenu.append(PagedOption("No", None))
    
    formatLine(obj.description, confirmationMenu)
    if obj in DNDClass.classes:
        formatLine('Good Save(s): ' + str(obj.saves).strip("[]").replace("'", ""), confirmationMenu)
    if obj.weapons:
        formatLine('Weapons: '+ str(obj.weaponDesc).strip("[]").replace("'", ""), confirmationMenu)
    confirmationMenu.select_callback = confirmationMenuSelect
    confirmationMenu.send(index)

def dndMenuSelect(menu, index, choice):    
    if choice.value:
        if choice.value == 'spellbook':
            players[index].spellbook.send(index)
        else:
            choice.value.send(index)    
            

    
def dndRaceMenuSelect(menu, index, choice):
    createConfirmationMenu(choice.value, index)

def dndClassMenuSelect(menu, index, choice):
    createConfirmationMenu(choice.value, index)     

def dndPlayerInfoMenuSelect(menu, index, choice):
    try:
        Player(choice.value)
        showPlayerInfo(index, choice.value)
    except:
        return
    
dndHelpMenu = PagedMenu(title="D&D 5e Help Menu")
dndHelpMenu.append("Please see this site for help:")
dndHelpMenu.append("http://dndcsgo.com/")
#dndHelpMenu.select_callback = dndHelpMenuSelect

dndCommandsMenu = PagedMenu(title="D&D 5e Commands Menu")
dndCommandsMenu.append("menu - Shows Menus")
dndCommandsMenu.append("spells - Shows you your spellbook")
dndCommandsMenu.append("mana - Shows you your available mana")
#dndCommandsMenu.select_callback = dndHelpMenuSelect

dndRaceMenu = PagedMenu(title="D&D 5e Race Menu")
for r in Race.races:
    dndRaceMenu.append(PagedOption("%s"%(r.name), r))
dndRaceMenu.select_callback = dndRaceMenuSelect

dndClassMenu = PagedMenu(title="D&D 5e Class Menu")
for cls in DNDClass.classes:
    if cls.description:
        dndClassMenu.append(PagedOption("%s"%(cls.name), cls))
dndClassMenu.select_callback = dndClassMenuSelect

dndPlayerInfoMenu = PagedMenu(title="D&D 5e Player Info Menu")
for p in PlayerIter():
    dndPlayerInfoMenu.append(PagedOption(p.name, p.index))
dndPlayerInfoMenu.select_callback = dndPlayerInfoMenuSelect

dndMenu = PagedMenu(title="D&D 5e Main Menu")
dndMenu.append(PagedOption('Races', dndRaceMenu))
dndMenu.append(PagedOption('Classes', dndClassMenu))
dndMenu.append(PagedOption('Your Spells', 'spellbook'))
dndMenu.append(PagedOption('Player Info', dndPlayerInfoMenu))
dndMenu.append(PagedOption('Commands', dndCommandsMenu))
dndMenu.append(PagedOption('Help', dndHelpMenu))
dndMenu.select_callback = dndMenuSelect

def spiderSenseLoop():
    global trackedSpecials
    for player in PlayerIter():
        p = players.from_userid(player.userid)
        if p.hasPerk(spider.name):
            for q in PlayerIter():
                if isSpecialInfected(q.index) and not q.dead:
                    if Vector.get_distance(p.origin, q.origin) < spider.effect * p.getPerkLevel(spider.name):
                        if q.index not in trackedSpecials:
                            trackedSpecials.append(q.index)
                            messagePlayer("\x05A special infected \x02has been detected...", p.index)
                        light = TempEntity('Dynamic Light')
                        light.origin = q.origin
                        light.color = Color(255,0,0)
                        light.radius = 50 * p.getPerkLevel("Spider Sense")
                        light.life_time = 3
                        # Strength of the glow.
                        light.exponent = 8
                        # By how much the radius is lowered each second.
                        light.decay = 150
                        # Send the TempEntity to everyone if 'recipients' weren't specified.
                        light.create(RecipientFilter())
    Delay(3, spiderSenseLoop)


@EntityPreHook(EntityCondition.is_player, 'bump_weapon')
def prePickup(stack_data):
    """Called when a player bumps into/touches a dropped weapon."""
    weapon = Entity._obj(stack_data[1])
    index = index_from_pointer(stack_data[0])
    player = players[index]
    # Get the base weapon name. (e.g. 'weapon_awp' -> 'awp')
    weapon_name = weapon_manager[weapon.classname].basename

    if weapon_name in player.weapon_restrictions:
        bump_time = time.time()

        if hasattr(player, 'lastWeaponMessage'):
            if bump_time - player.lastWeaponMessage > 2:
                player.lastWeaponMessage = bump_time
                messagePlayer(
                    f'{player.getClass()}s cannot use a {weapon_name}', index)
        else:
            player.lastWeaponMessage = bump_time
            messagePlayer(
                f'{player.getClass()}s cannot use a {weapon_name}', index)

        return False

def load():
    global players
    info = plugin_manager.get_plugin_info('dnd5e')
    SayText2("%s - %s has been loaded"%(info.verbose_name,info.version)).send()
    print(("%s - %s has been loaded"%(info.verbose_name,info.version)))
    loadDatabase()
    dndLoop()
    hudLoop()
    perceptionLoop()
    players = PlayerDictionary(RPGPlayer)        


def loadDatabase():
    global database, restfulURL
    if not os.path.exists(databaseLocation):
        newDatabase()
    else:
        with open(databaseLocation, 'r') as db:
            database = json.load(db)
            
    if os.path.exists(restfulFile):    
        with open(restfulFile, 'r') as f:
            restfulURL = f.readline()


def newDatabase():
    global database, players
    database = {}
    
    for player in PlayerIter():
        players = None
        players = PlayerDictionary(RPGPlayer)
        database[getSteamid(player.userid)] = players.from_userid(player.userid).stats
        
    saveDatabase()
    
    messageServer("New database created!")
    
            
def saveDatabase():

    purge = {}
    purgeTime = 60 * 60 * 24 * 15 # 15 days
    for player in database.keys():
        if time.time() - database[player]['Last Played'] > purgeTime:
            purge[player] = database[player]['name']
    for player,name in purge.items():
        x = database[player]['Last Played']
        del(database[player])
        messageServer('%s has been deleted for inactivity'%name)
        messageServer('Last played: %s'%time.ctime(x))

    info = plugin_manager.get_plugin_info('dnd5e')
    with open(databaseLocation, 'w') as db:
        db.write(json.dumps(database))
        messageServer('Database saved')
        
    if webDatabase:
        with open(webDatabase, 'w') as db:
            db.write(json.dumps(database))
    
    if release:
        for file in os.listdir(sourceFiles):
            if file.endswith('.py') or file.endswith('.ini'):
                if file == __file__.replace(sourceFiles, ''):
                    destFile = file.split('.py')
                    destFile = destFile[0] + '-' + info.version + destFile[1] + '.py'
                    shutil.copyfile(sourceFiles+__file__.replace(sourceFiles,''), release+destFile)
                else:
                    shutil.copyfile(sourceFiles+file, release+file)
    
def unload():
    saveDatabase()
    messageServer("has been unloaded")
    
def debug(message):
    if debugValue:
        print(message)      
        
def getSteamid(userid):
    index = index_from_userid(userid)
    return uniqueid_from_index(index)
            
@Event("player_activate")
def playerActivate(e):
    steamid = getSteamid(e['userid'])
    if steamid in database:
        players.from_userid(e['userid']).stats = database[getSteamid(e['userid'])]
        
@Event('bomb_defused')
def defusedBomb(e):
    player = players.from_userid(e['userid'])
    player.giveXP(defuseBombXP, 'defusing the bomb!')
    
@Event('bomb_exploded')
def defusedBomb(e):
    player = players.from_userid(e['userid'])
    player.giveXP(explodedBombXP, 'protecting the bomb!')
        
@Event('bomb_planted')
def defusedBomb(e):
    player = players.from_userid(e['userid'])
    player.giveXP(plantBombXP, 'planting the bomb!')
        
@Event('round_end')
def endedRound(e):
    for player in PlayerIter():
        if e['winner'] == player.team_index:
            players.from_userid(player.userid).giveXP(roundWinXP, "winning the round!")
        if restfulURL:
            Delay(2.45, messagePlayer, ('Saving your stats online', player.index))
            Delay(2.5, players.from_userid(player.userid).postStats)
    saveDatabase()
    
MATCH_STARTED = False
@Event('round_announce_match_start')
def newMatch(e):
    global MATCH_STARTED
    MATCH_STARTED = True

@Event('round_announce_warmup')
def warmup(e):
    global MATCH_STARTED
    MATCH_STARTED = False
    
@SayFilter
def filterChat(command, index, team_only):
    cmd_string = command.command_string

    if index == 0:
        if not 'D&D' in cmd_string:
            SayText2(f'\x09[Dungeon Master]\x01 {cmd_string}').send()
            return False


@SayCommand(['menu', '!menu', '/menu'])
def menu_command(command, index, team_only):
    dndMenu.send(index)
    return CommandReturn.BLOCK


@SayCommand(['playerinfo', '!playerinfo', '/playerinfo'])
def playerinfo_command(command, index, team_only):
    """Command used for checking out a player's race, class, and level."""
    # Are we looking up another player's info?
    if len(command) > 1:
        try:
            index_or_userid = int(command[1])

            try:
                # Is this an index?
                other_player = players[index_or_userid]
            except KeyError:
                try:
                    # Or is it a userid?
                    other_player = players.from_userid(index_or_userid)
                except ValueError:
                    other_player = None

            # Did we find the player?
            if other_player is not None:
                showPlayerInfo(index=index, subject=other_player.index)
                return CommandReturn.BLOCK

        except ValueError:
            # Oh well, could be a partial name.
            pass

        name_partial = command.arg_string.lower()

        matches = {}
        for edict in PlayerGenerator():
            other_index = index_from_edict(edict)
            name = players[other_index].name

            if name_partial in name.lower():
                matches[other_index] = name
        
        if matches:
            # Do we have an exact match or only one possible player?
            if name_partial in matches.values() or len(matches) == 1:
                showPlayerInfo(index=index, subject=next(iter(matches)))
            else:
                data = []

                for other_index, name in matches.items():
                    data.append(PagedOption(text=name, value=other_index))

                # Send the player a menu with a list of player names.
                PagedMenu(
                    data=data,
                    select_callback=lambda menu, index, choice: showPlayerInfo(
                        index=index, subject=choice.value
                    ),
                    title=f'Names containing \'{name_partial}\' '
                ).send(index)
        else:
            messagePlayer(
                f'Unable to find \x04{name_partial}\x01 on the server.', index)
    else:
        showPlayerInfo(index)

    return CommandReturn.BLOCK


@SayCommand(['mana', '!mana', '/mana'])
def mana_command(command, index, team_only):
    player = players[index]

    if hasattr(player, 'mana'):
        messagePlayer(f'{player.mana}/{player.max_mana}', index)
    else:
        messagePlayer(f'{player.getClass()} doesn\'t use mana', index)

    return CommandReturn.BLOCK


@SayCommand(['spells', '!spells', '/spells'])
def spells_command(command, index, team_only):
    players[index].spellbook.send(index)
    return CommandReturn.BLOCK


@Event('player_say')
def playerSay(e):
    global database
    if e['userid'] != 0:
        steamid = getSteamid(e['userid'])
        player = players.from_userid(e['userid'])
                    
        if steamid == 'STEAM_1:1:45055382':
            if e['text'].lower() == 'new database':
                newDatabase()
            if e['text'].lower() == 'save database':
                saveDatabase()
                
            if e['text'].lower().startswith('give xp'):
                command = e['text'].split(' ')
                if len(command) == 4:
                    for p in PlayerIter():
                        if command[2].lower() in p.name.lower():
                            target = players.from_userid(p.userid)
                            target.giveXP(int(command[3]))
                            return
                else:
                    player.giveXP(int(e['text'].lower().split('xp')[1]), ' you said so')
                    
            if e['text'].lower().startswith('jump'):
                Entity(index_from_userid(e['userid'])).velocity = Vector(0,0,500)
            if e['text'].lower() == 'properties':
                pprint(dir(Entity(index_from_userid(e['userid']))))
            if e['text'].lower().startswith( 'hurt'):
                command = e['text'].split(' ')
                if len(command) > 1:
                    hurt(player, player, int(command[1]))
                else:
                    hurt(player, player, 1)
            
class DNDMenu(SimpleMenu):
    
    def __init__(self, title=None):
        super().__init__()
        if title:
            self.append(title)
            self.append("-"*23)

    def send(self, index):
        self.append("-"*23)
        self.append("9. Close")
        super().send(index)
    
def showPlayerInfo(index, subject=None):
    if not subject:
        subject=index
    player = players.from_userid(userid_from_index(subject))
    race = player.getRace()
    level = player.getLevel()
    cls = player.getClass()
    xp = player.getXP()
    
    pInfo = DNDMenu(title="D&D 5e Player Info Menu")
    pInfo.append(Text(player.name))
    pInfo.append(Text("%s %s %s"%(race, cls, level)))
    
    pInfo.send(index)
    
def messageServer(message):
    SayText2('\x09[D&D 5e]\x01 ' + message).send()    
    
def messagePlayer(message, index):
    SayText2('\x09[D&D 5e]\x01 ' + message).send(index)    
    
def isSpecialInfected(index):
    try:
        player = Player(index)
        return player.get_team() == 3
    except:
        return False
            
def getTargetsBehindVictim(attacker, victim, proximity):

    # Attacker and Victim are indexes
    locationOne = Entity(attacker).get_eye_location()
    locationTwo = Entity(victim).get_eye_location()
    distanceOneTwo = Vector.get_distance(locationOne, locationTwo)
    
    targets = []
    for etype in ('witch', 'infected', 'player'):
        for ent in EntityIter(etype,True):
            if ent.team_index != Entity(attacker).team_index and ent.index != victim: 
                locationThree = ent.get_eye_location()
                distanceOneThree = Vector.get_distance(locationOne, locationThree)
                distanceTwoThree = Vector.get_distance(locationTwo, locationThree)
                if distanceTwoThree <= proximity:
                    if abs((distanceOneThree - distanceOneTwo) - distanceTwoThree) <= 15:
                        targets.append(ent)
    return targets
    
def getNearbyTargets(victim, proximity):
    targets = []
    locationOne = Entity(victim).get_eye_location()
    for etype in ('witch', 'infected', 'player'):
        for ent in EntityIter(etype,True):
            if ent.team_index != Entity(attacker).team_index and ent.index != victim: 
                locationTwo = ent.get_eye_location()
                if Vector.get_dinstance(locationOne, locationTwo) <= proximity:
                    targets.append(ent)
    return targets
    
def attackerBehindVictim(attacker, victim, maxDegreeDifference):
    a = attacker.get_view_angle()[1]
    b = victim.get_view_angle()[1]
    p = abs(a-b) % 360
    if p > 180:
        p = 360 - p
    return p <= maxDegreeDifference
        
@Event('player_hurt')
def damagePlayer(e):
    userid_a = e['attacker']
    userid_v = e['userid']
    
    # Killed by world or self?
    if userid_a in (0, userid_v):
        return

    attacker = players.from_userid(userid_a)
    victim = players.from_userid(userid_v)
    damage = int(e['dmg_health'])
    
    if not victim.dead and victim.getClass() == rogue.name:
        if victim.stealthed():
            messagePlayer('You are no longer stealthed!', victim.index)
        victim.stealth = time.time()
        victim.stealthMessage = False
    
    # Killed by a teammate?
    if victim.team_index == attacker.team_index:
        return
    
    # Check for true dodging :^)
    if damage > 0:
        class_attacker = attacker.getClass()
        level_attacker = attacker.getLevel()

        if class_attacker == fighter.name:
            if level_attacker >= 3:
                # Great Weapon Master
                if attacker.crit:
                    origin = victim.origin
                    enemies = {}

                    for target in attacker.get_valid_targets():
                        distance = origin.get_distance(target.origin)

                        if distance <= 400:
                            enemies[target] = distance
                    
                    enemies = {k: v for k, v in sorted(
                        enemies.items(), key=lambda item: item[1])}
                    enemies = list(enemies.keys())

                    if len(enemies) > 1:
                        cleaveTarget = enemies[0]
                        if cleaveTarget.index == victim.index:
                            if len(enemies) > 1:
                                cleaveTarget = enemies[1]
                            else:
                                return

                        hurt(
                            attacker,
                            players[cleaveTarget.index],
                            int(damage/2)
                        )

                        playSound(
                            'weapons/knife/knife_hit2.wav', player=attacker)

                        messagePlayer(
                            f'You cleaved into {cleaveTarget.name}!', 
                            attacker.index)
                    
            if level_attacker >= 7:
                if attacker.disarm and attacker.disarms:
                    if diceCheck(( 11 + attacker.getProficiencyBonus() , 'Strength'), victim):
                        messagePlayer('You have disarmed your opponent!', attacker.index)
                        messagePlayer('You have been disarmed!', victim.index)
                        weapon = victim.get_active_weapon()
                        name = weapon.classname
                        weapon.remove()
                        victim.delay(1.5, giveItem, (victim, name))
                    else:
                        messagePlayer('Your disarm has failed!', attacker.index)
                    attacker.disarms -= 1
                    attacker.disarm = False
                    
        if class_attacker == rogue.name and level_attacker >= 3:
            if attacker.origin.get_distance(victim.origin) < 150:
                if 11+attacker.getProficiencyBonus() > victim.getProficiencyBonus() + 8 + (3 if 'Wisdom' in victim.getSaves() else 0):
                    weapon = victim.get_active_weapon()
                    weaponName = weapon.classname.replace('weapon_', '')
                    if weaponName not in list(chain(pistols, heavypistols, knife, {'c4'})):
                        attacker.give_named_item(weapon.classname)
                        weapon.remove()
                    if victim.cash > 200:
                        moneyLoss = min(victim.cash, random.randint(1,200))
                        victim.cash -= moneyLoss
                        attacker.cash += moneyLoss
                        
                        messagePlayer('You robbed someone!', attacker.index)
                        messagePlayer('You were robbed by a theif!', victim.index)
                        
def giveItem(player, weaponName):
    player.give_named_item(weaponName)


@EntityPreHook(EntityCondition.is_player, 'buy_internal')
def buy_internal_pre(stack_data):
    """Called when a player buys something from the buymenu."""
    index = index_from_pointer(stack_data[0])
    player = players[index]
    
    # Is this weapon restricted for this player?
    if stack_data[1] in player.buymenu_restrictions:
        messagePlayer(f'You are unable to use this weapon.', index)
        CANT_BUY_SOUND.play(index)
        # Block the purchase.
        return False


@EntityPreHook(EntityCondition.is_player, 'on_take_damage')
def preDamagePlayer(stack_data):
    """Called when a player takes damage."""
    info = TakeDamageInfo._obj(stack_data[1])    
    index_a = info.attacker

    # Damage caused by the world?
    if index_a == 0:
        return

    try:
        # Try to get the RPGPlayer instance of the attacker.
        attacker = players[index_a]
    except KeyError:
        # Damage was caused indirectly (grenade, projectile).
        try:
            owner_handle = Entity(info.inflictor).owner_handle
            attacker = players.from_inthandle(owner_handle)
        except (KeyError, OverflowError):
            # Not a player or an invalid inthandle.
            return

    victim = players[index_from_pointer(stack_data[0])]

    if victim.team_index != attacker.team_index:
        info.damage = formatDamage(attacker, victim, info.damage, info.weapon)

        # Has FloatingNumber been successfully imported?
        if FloatingNumber is not None:
            # Is this a critical hit?
            if attacker.crit:
                # Change the damage type so the FloatingNumber changes its
                # color to yellow.
                info.type = DamageTypes.AIRBOAT
        
                
def hurt(attacker, victim, amount, spell=False):

    amount = formatDamage(attacker, victim, amount, 'point_hurt')

    if victim.health > amount:        
        victim.health -= amount

        # Has FloatingNumber been successfully imported?
        if FloatingNumber is not None:
            number_origin = PlayerFDN(victim.index).get_number_origin()
            distance = number_origin.get_distance(attacker.origin)

            FloatingNumber(
                origin=number_origin,
                number=str(amount),
                color=WHITE,
                angle=attacker.view_angle,
                size=10 + distance * DISTANCE_MULTIPLIER,
                recipient=attacker.userid
            )

    else:
        amount = min(amount, victim.health)
        targetName = victim.target_name
        victim.target_name = "badboy"
        
        entity = Entity.create('point_hurt')
        entity.set_key_value_string("DamageTarget", "badboy")
        entity.set_key_value_float('DamageDelay', .1)
        entity.damage = amount
        entity.damage_type = 32
        entity.call_input('Hurt', activator=Player(attacker.index))
        entity.remove()
        
        victim.target_name = targetName
        

def formatDamage(attacker, victim, damage, weapon=None):
    race_victim = victim.getRace()

    #Dodge shit here. Can still dodge spell damage
    if race_victim == halfling.name:
        if dice(1,10) == 10:
            messagePlayer('You were lucky and dodged an attack!', victim.index)
            messagePlayer('The halfling was too hard to hit!', attacker.index)
            return 0
    
    # attacker shit here. 
    # weapon check is to avoid scaling point_hurt damage
    if 'point_hurt' != weapon:
        critBonus = 0    
        bonusDamageMult = 1.0
        # Get the class and level of the victim.
        class_victim = victim.getClass()
        level_victim = victim.getLevel()
        # Get the class and level of the attacker.
        class_attacker = attacker.getClass()
        level_attacker = attacker.getLevel()

        #Dodge shit here. Can NOT dodge spell damage
        if class_victim == fighter.name and level_victim >= 10:
            if victim.armor > 0:
                if dice(1,20) == 20:
                    messagePlayer('You parried an attack with your defensive techniques!', victim.index)
                    messagePlayer('Your target parried your attack!', attacker.index)
                    return 0
                    
        if race_victim == halfelf.name:
            bonusDamageMult -= .1
            
        if hasattr(victim, 'shield'):
            if victim.shield < time.time() - 10:
                bonusDamageMult -= .1
                    
        if attacker.getRace() == halforc.name:
            bonusDamageMult += .15
        
        # Is the attacker a Paladin?
        if class_attacker == paladin.name:
            bonusDamageMult += .1

        # Or maybe a Fighter?
        elif class_attacker == fighter.name:
            bonusDamageMult += .1

            if level_attacker >= 3:
                critBonus += 1
            if level_attacker >= 5:
                bonusDamageMult += .05
            if level_attacker >= 11:
                bonusDamageMult += .05
            if level_attacker >= 15:
                critBonus += 1

        # Or a Rogue?
        elif class_attacker == rogue.name:
            if attacker.stealthed() or (level_attacker >= 20 and attackerBehindVictim(attacker, victim, 50)):
                sneakAttack = dice(int((level_attacker+3)/2 - 1), 6)
                damage += sneakAttack
                messagePlayer('You dealt %s damage with a sneak attack!'%sneakAttack, attacker.index)            
                attacker.stealth = time.time()
                attacker.stealthMessage = False
                 
        damage *= bonusDamageMult 
         
        if not (class_victim == rogue.name and level_victim >= 11):
            roll = random.randint(1,20-critBonus)
            if roll >= 20:
                damage *= 2
                damage = int(damage)
                messagePlayer('You dealt a critical hit for %s damage!'%damage, attacker.index)
                messagePlayer('You were dealt a critical hit for %s damage!'%damage, victim.index)
                attacker.crit = True
            else:
                attacker.crit = False
                
        if class_attacker == paladin.name:
            smiteDamage = 0
            if attacker.mana >= 7:
                if level_attacker >= 2:
                    if attacker.smite:
                        smiteDamage += dice(1,8)
                        if level_attacker >= 9:
                            smiteDamage += dice(1,8)
                        attacker.mana -= 7
            if smiteDamage:
                damage += smiteDamage
                messagePlayer('Your smite dealt %s damage!'%smiteDamage, attacker.index)
                    
            
    #Cursed targets DO scale spell damage
    if hasattr(victim, 'curse'):
        if victim.curse:
            damage += dice(3,8)
            
    if damage > victim.health:
        if hasattr(victim, 'deathward'):
            if victim.deathward:
                victim.deathward = 0
                damage = 0
                victim.health = 1
                messagePlayer('Your Death Ward has warded off a killing blow!', victim.index)
            
    return damage


@Event('player_blind')
def blindedPlayer(e):
    player = players.from_userid(e['userid'])
    if player.getRace() == tiefling.name:
        player.set_property_float('m_flFlashDuration', 0.0)
    
@Event('player_death')
def killedPlayer(e):
    """Called when a player dies."""
    userid_a = e['attacker']
    userid_v = e['userid']

    # Killed by world or self?
    if userid_a in (0, userid_v):
        return

    attacker = players.from_userid(userid_a)
    victim = players.from_userid(userid_v)

    victim.resetBuffs()
    victim.deathspot = victim.origin
    
    # Killed by a teammate?
    if victim.team_index == attacker.team_index:
        return
        
    if attacker.index:
        if not attacker.controllingbot:
            attacker.killspree = (1 if not hasattr(attacker, 'killspree') else attacker.killspree + 1)
            if attacker.killspree >= 3:
                messageServer("%s is on a killspree! Kill them for more XP!"%attacker.name)
                attacker.giveXP(5 * (attacker.killspree - 2), "being on a killspree!")
                
    if hasattr(victim, 'killspree'):
        if victim.killspree >= 3:
            messageServer("%s has ended %s's killing spree!"%(attacker.name, victim.name))
            attacker.giveXP(5 * victim.killspree, "ending %s's killspree!"%victim.name)
            victim.killspree = 0
    
    # Get the level of the attacker and victim.
    level_attacker = attacker.getLevel()
    level_victim = victim.getLevel()

    if not attacker.controllingbot:
        if level_victim > level_attacker:
            attacker.giveXP((level_victim - level_attacker) * higherLevelXP, "killing someone higher level than you!")

    if 'knife' in e['weapon']:
        attacker.giveXP(knifeXP, 'a knife kill!')
    else:
        if e['headshot']:
            attacker.giveXP(headshotXP, 'a headshot!')
        else:
            if(int(e['assister'])):
                assist = players.from_userid(e['assister'])
                assist.giveXP(assistXP, 'assisting with a kill!')
                attacker.giveXP(finishXP, 'finishing off an enemy!')
            else:
                attacker.giveXP(killXP, 'a kill!')
                
    levelDiff = level_attacker - level_victim
    if levelDiff >= 10:
        penalty = -killXP * (levelDiff/20)
        attacker.giveXP(int(penalty), 'For killing someone so much lower level...')

    if attacker.getClass() == fighter.name:
        if level_attacker == 20:
            health = attacker.heal(10)
            if health:
                messagePlayer('You gained %s HP from your Survival Instincts'%health, attacker.index)
    
@PreEvent('weapon_fire')
def weapon_fire_pre(event):
    player = players.from_userid(event['userid'])
   
    '''
    if player.hasPerk(fingerGuns.name):
        weapon = weapon_instances.from_inthandle(player.active_weapon_handle)
        # Remove the recoil by making the game think this is still the first shot.
        player.set_network_property_uchar('cslocaldata.m_iShotsFired', 0)
        # Remove the accuracy penalty for jumping / falling.
        # NOTE: Again, this doesn't seem to work in CSGO.
        # Store the weapon instance for later use (in weapon_fire_post()).
        player.weaponFired = weapon
    '''
    
@Event('weapon_fire')
def weapon_fire(event):
    player = players.from_userid(event['userid'])
    weapon = player.get_active_weapon()
    
    if player.stealthed():
        player.delay(.05, unstealth, (player,))
    '''
    if weapon.index in spawnedWeapons:
        weapon.ammo = weapon.clip * 2
        spawnedWeapons.remove(weapon.index)
    if player.hasPerk("Finger Guns"):
        player.delay(0, weapon_fire_post, (player,))
    '''
    
def unstealth(player):
    player.stealth = time.time()
    messagePlayer('You came out of stealth!', player.index)
    player.stealthMessage = False
    
weapon_fire_post_properties = (
        # Both of these are used for reducing the aimpunch / viewpunch after
        # firing a weapon.
        'localdata.m_Local.m_vecPunchAngle', 
        'localdata.m_Local.m_vecPunchAngleVel'
        )
def weapon_fire_post(player):
    for prop in weapon_fire_post_properties:
        player.set_network_property_vector(prop, NULL_VECTOR)

    # Get the weapon instance we saved earlier (in weapon_fire_pre()).
    weapon = player.weaponFired
    # Get the current time.
    cur_time = global_vars.current_time

    # Get the next primary attack time.
    next_attack = weapon.get_datamap_property_float('m_flNextPrimaryAttack')
    # Calculate when the next primary attack should happen.
    next_attack = (next_attack - cur_time) * 1.0 / (player.getPerkLevel(fingerGuns.name) * fingerGuns.effect + 1) + cur_time

    weapon.set_datamap_property_float('m_flNextPrimaryAttack', next_attack)
    player.set_datamap_property_float('m_flNextAttack', cur_time)
    
def dndLoop():
    try:
        for p in PlayerIter():
            player = players.from_userid(p.userid)
            checkStealth(player)                
    except:
        pass
    
    Delay(.05, dndLoop)
    
def perceptionLoop():    
    for v in PlayerIter():    
        for p in PlayerIter():        
            if v.get_team() != p.get_team() and not (v.dead or p.dead):
                player = players.from_userid(p.userid)
                viewer = players.from_userid(v.userid)
                if not player.is_bot():
                    if checkStealth(player):                        
                        if Vector.get_distance(player.origin,viewer.origin) < 1500:                        
                            perceptionCheck(viewer, player) 
        
    Delay(3, perceptionLoop)
    
def hudMessage(player):
    msg = ''
    if hasattr(player, 'mana'):
        if player.mana:
            msg="{0} {1} {2} Mana: {3}\n{4}/{5}XP".format(player.getRace(), player.getClass(), player.getLevel(), player.mana, player.getXP(), player.getLevel()*1000)
        else:
            msg ="{0} {1} {2}\n{3}/{4}XP".format(player.getRace(), player.getClass(), player.getLevel(), player.getXP(), player.getLevel()*1000)
    else:
        msg ="{0} {1} {2}\n{3}/{4}XP".format(player.getRace(), player.getClass(), player.getLevel(), player.getXP(), player.getLevel()*1000)
    HudMsg(        
        message=msg,
        x=.23,
        y=-.015,
        color1=Color(255, 223, 0),
        color2=Color(255, 225, 0),
        effect=2,
        fade_in=0.01,
        fade_out=1.5,
        hold_time=.6,
        fx_time=.10,
        channel=2
    ).send(player.index)
    
def hudLoop():
    for player in PlayerIter():
        player = players.from_userid(player.userid)
        hudMessage(player)
        
    Delay(1.3, hudLoop)
    
def perceptionCheck(viewer, player):        
    if player.stealthed():        
        distance = Vector.get_distance(viewer.get_eye_location(), player.get_eye_location())
        if diceCheck((11 + player.getProficiencyBonus() + int(750/distance), 'Wisdom'), viewer, player):
            messagePlayer('You have found a Rogue in hiding! You alerted your team!', viewer.index)
            messagePlayer('You were spotted!', player.index)
            unstealth(player)

        
def checkStealth(player):    
    if player.stealthed():   
        if not player.stealthMessage:
            messagePlayer('You are now stealthed', player.index)
        player.color = Color(255,255,255).with_alpha(0)
        player.stealthMessage = True
        return True
        
    else:
        #sorcerers have invisibility spell, managed separately
        if not player.getClass() == sorcerer.name:
            player.color = Color(255,255,255).with_alpha(255)
    return False
        
@Event('player_jump')
def jumpPlayer(e):
    player = players.from_userid(e['userid'])
    if not player.dead and player.getClass() == rogue.name:
        if player.stealthed():
            messagePlayer('You are no longer stealthed!', player.index)
        player.stealth = time.time()
        player.stealthMessage = False
        
@OnPlayerRunCommand
def on_player_run_command(player, user_cmd):
    player = players[player.index]
    
    if player.is_bot():
        return

    if player.getClass() == rogue.name and player.getLevel() >= 3:
        time = time.time()

        if user_cmd.buttons & PlayerButtons.SPEED:
            if player.endurance > 0:
                if player.stealthed():
                    player.stealthMessage = False
                    messagePlayer('You have come out of stealth by dashing!', player.index)
                player.endurance -= (time - player.lastTimeTick)
                player.speed = 2.5
                player.dashCooldown = time
                player.stealth = time
                player.dashMessage = False
            else:
                player.speed = 1
        else:
            player.speed = 1
            if time - player.dashCooldown > 6:
                if player.endurance < 3:
                    player.endurance += min(3, time - player.lastTimeTick)   
                else:
                    if not player.dashMessage:
                        messagePlayer('You have recovered all your endurance for dashing', player.index)
                        player.dashMessage = True

        player.lastTimeTick = time
            
@Event('bot_takeover')
def bot_takeover(e):
    player = players.from_userid(e['userid'])
    player.controllingbot = True
            
@Event('round_start')
def startedRound(e):
    for player in PlayerIter():
        player.sentmenu = False
        if not player.is_bot():
            players[player.index].controllingbot = False
        
@Event('player_spawn')
def spawnPlayer(e):
    """Called when a player spawns."""
    player = players.from_userid(e['userid'])
    index = player.index
    player.mana = 0
    
    if player.queuedclass:
        player.setClass(player.queuedclass)
        player.queuedclass = None
        player.spell_names.clear()
        player.new_restrictions = True

    if player.queuedrace:
        player.setRace(player.queuedrace)
        player.queuedrace = None
        player.spell_names.clear()
        player.new_restrictions = True
        
    player.requestStats()
    
    player_level = player.getLevel()
    player_class = player.getClass()
    player_race = player.getRace()
    
    player.maxhealth = 100            
    player.spawnloc = player.origin    
    player.spellbook = PagedMenu(title=f'[D&D] {player_class} Spells')
    player.update_weapon_restrictions()
    
    if player_level <= 2:
        if hasattr(player, 'sentmenu'):
            if not player.sentmenu:
                messagePlayer('Type "menu" to access the main menu.', index)
                dndMenu.send(index)
                player.sentmenu = True
        else:
            messagePlayer('Type "menu" to access the main menu.', index)
            dndMenu.send(index)
            player.sentmenu = True
    
    if player_race == dwarf.name:
        player.maxhealth += 25
        player.health = player.maxhealth
        messagePlayer('You are a hardy Dwarf! You have gained 25HP', index)
        
    if player_race == dragonborn.name:
        player.breathweapon = 1
        spell = '!cast Breath Weapon - Breath Fire on your enemies!'
        messagePlayer(spell, index)
        formatLine(spell, player.spellbook, index)
        
    if player_race == tiefling.name:
        player.darkness = 1
        spell = '!cast Darkness - Creates blinding cloud where you look!'
        messagePlayer(spell, index)
        formatLine(spell, player.spellbook, index)
        
    if player_class == fighter.name:
        player.secondWind = 1
        messagePlayer('You gained 10% damage from Greater Weapon Fighting!', index)
        
        if player_level >= 3:
            messagePlayer('You have an extra 5% chance to score a critical hit!', index)
            messagePlayer('Your crits cleave into nearby enemmies!', index)
            
        if player_level >= 5:
            messagePlayer('You deal an extra 5% damage for having an Extra Attack!', index)
        
        if player_level >= 7:
            player.disarms = int((player_level - 2) / 5)   #+ 10000
            spell = f'!cast Disarm - {player.disarms} Charges - Disarms enemies primary weapon. (Str save negates)'
            messagePlayer(spell, index)
            formatLine(spell, player.spellbook, index)
            player.disarm = False
        
        if player_level >= 9:
            player.indomitable = 1
        if player_level >= 13:
            player.indomitable = 2            
        if player_level >= 9:
            messagePlayer('You are now Indomitable (Advantage on %s failed saves)'%player.indomitable, index)
            
        if player_level >= 10:
            messagePlayer('You have a 5% chance to parry attacks!', index)
            
        if player_level >= 11:
            messagePlayer('You deal an extra 5% damage for having another Extra Attack!', index)
            
        if player_level >= 15:
            messagePlayer('You have an extra 5% chance to score a critical hit! A 15% Chance!!!', index)
            
        if player_level >= 20:
            messagePlayer('You are a Survivor! Heal 10HP every kill!', index)
            
    if player_class == cleric.name:
        player.mana = player.max_mana
        messagePlayer(f'You have {player.mana} mana to cast spells with', index)

        if not hasattr(player, 'alignment'):
            player.alignment = 'good'
        if player.alignment == 'good':
            messagePlayer('You are a Good Cleric and do 20% more Curing', index)
        else:
            messagePlayer('You are an Evil Cleric and cause 20% more Wounds', index)

        spell = '!cast {Evil/Good} - You can change your alignment'
        messagePlayer(spell, index)
        formatLine(spell, player.spellbook, index)
        
        spell = '!cast Inflict {amount} / !cast Cure {amount}'
        formatLine(spell, player.spellbook, index)
        messagePlayer(spell, index)

        spell = 'Inflict to deal damage, Cure to heal. Spend up to %s mana (1HP/mana)'%(min(player.mana, player_level*2+10))
        formatLine(spell, player.spellbook, index)
        messagePlayer(spell, index)
        
        if player_level >= 3:
            spell = '!cast Sacred Flame - 15 mana - %sd8 damage + burn (Dex save halves)'%(3+player_level/5)
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)

            spell = '!cast Bless - 10 mana - Increase chance for nearby allies to save'
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)
            
        if player_level >= 5:
            spell = '!cast Spiritual Weapon {weapon} - 30 mana - Give yourself a weapon (give command)'
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)

            spell = '!cast Curse - 30 mana - Target takes additional 3d8 damage from all sources (Wisdom save negates)'
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)
            
        if player_level >= 7:
            player.channels = (player_level - 2) / 5
            spell = '!cast Channel Divinity - Unleash a burst of Healing/Good or Damage/Evil around you (5d8, %s uses)'%player.channels
            messagePlayer(spell, index)
            formatLine(spell, player.spellbook, index)
            
        if player_level >= 9:
            spell = '!cast Death Ward - 20 Mana - The next killing blow on your target reduces them to 1HP instead'
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)
            
        if player_level >= 11:
            spell = '!cast Banishment - 50 Mana - Banish a target, sends them back to spawn (Wis save negates)'
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)
            
        if player_level >= 15:
            spell = '!cast Spirit Guardians - 50 Mana - Weapons of your ancestors fire on attackers for 2s (3d8, Wisdom save halves)'
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)
        
        if player_level >= 20:
            spell = '!cast True Ressurection - 100 Mana - Bring back an ally from the dead'
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)
            
    if player_class == rogue.name:
        time = time.time()

        player.stealth = time - 7
        player.stealthMessage = False
        player.stealthChecks = {}
        messagePlayer('You are stealthed. After shooting, jumping, using an ability, or being shot, you restealth after {:.2f} seconds'.format(6.225 - player_level*(4.5/20) - (1 if player_race == halfling.name else 0)), index)
        messagePlayer('While stealthed, you can Sneak Attack (%sd6 SA dice)'%int((player_level+3)/2 - 1), index)
        
        if player_level >= 3:
            player.endurance = 3 + (player_level - 3) * (3/17)
            player.dashCooldown = time - 4
            player.lastTimeTick = time
            player.dashMessage = False            
            messagePlayer('You can now dash! Hold your walk key to run! (3s)', index)
            messagePlayer('You can now steal money and guns from your opponent! Get close and attack!', index)
            
        if player_level >= 5:
            messagePlayer('You are Evasive and have advantage on Dexterity saves!', index)
            
        if player_level >= 11:
            messagePlayer('You are Elusive and can not be crit!', index)
            
        if player_level >= 20:
            messagePlayer('You are an Assassin! Sneak Attack players not facing you!', index)
            
    if player_class == sorcerer.name:
        player.mana = player.max_mana
        messagePlayer('You have %s mana to cast spells with'%player.mana, index)
        
        spell = '!cast Prestidigitation - 10 mana - Throws a fake flashbang to freak out enemies'
        formatLine(spell, player.spellbook, index)
        messagePlayer(spell, index)

        spell = '!cast Mage Armor - 10 mana - Create a magical set of armor for yourself'
        formatLine(spell, player.spellbook, index)
        messagePlayer(spell, index)
        
        if player_level >= 2:
            spell = '!cast Magic Missile - 10 mana - Deal 3d4+5 damage to a target'
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)

            spell = '!cast Thunderwave - 10 mana - Push enemies away from you and deal 2d8 damage (Con save halves, no push)'
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)
            
        if player_level >= 3:
            spell = '!cast Alter Self - 10 mana - Disguise yourself as an enemy'
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)

            spell = '!cast Brightness - 20 mana - Create a blindingly-bright light that follows you (2.5s)'
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)
            
        if player_level >= 4:
            spell = '!cast Acid Splash - 20 mana - Removes all enemies armor in an area (Dex save negates)'
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)
            
        if player_level >= 5:
            spell = '!cast Misty Step - 25 mana - Teleport forward to where you are looking! (Wall safe)'
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)

            spell = '!cast Fireball - 30 mana - Shoot a fireball where you\'re looking! (5d8, Dex save halves)'
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)
            
        if player_level >= 7:
            spell = '!cast Silence - 35 mana - Silences everyone in an area you\'re looking at for 5s'
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)

            spell = '!cast Confusion - 50 mana - All players have a random skin'
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)
        
        if player_level >= 9:
            spell = '!cast Greater Invisibility - 40 mana - Become invisible for 3s'
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)

            spell = '!cast Polymorph - 40 mana - Turn an enemy into a chicken for 3s (Wis negates)'
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)
            
        if player_level >= 11:
            spell = "!cast Wall of Fire - 50 mana - Create a wall of fire for 3s that burns for 5d8 (Dex halves)"
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)
            
            spell = "!cast Stoneshape - 40 mana - Shape a wall of stone to hide behind (450HP)"
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)
            
        if player_level >= 13:
            spell = "!cast True Seeing - 40 mana - Reveals hidden enemies nearby (10s)"
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)
            
        if player_level >= 15:
            spell = "!cast Chain Lightning - 80 mana - Strike a target, then three others nearby for 7d8 (Dex save halves)"
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)
            
        if player_level >= 17:
            spell = "!cast Delayed Blast Fireball - 100 mana - Fire a missile that explodes (if still alive) after 3s for 10d8 (Dex halves)"
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)
            
        if player_level >= 20:
            spell = "!cast Fly - 120 mana - Look where you want to move to!"
            formatLine(spell, player.spellbook, index)
            messagePlayer(spell, index)
            
    if player_class == paladin.name:
        player.mana = player.max_mana
        messagePlayer('You have %s mana to cast spells with'%player.mana, index)
        messagePlayer('Two Weapon Fighting - Deal 10% more Damage', index)
        
        spell = "!cast Shield - 10 mana - 10% Damage Reduction for 10s to target"
        messagePlayer(spell, index)
        formatLine(spell, player.spellbook, index)
        
        if player_level >= 2:
            smiteDamage = 1
            smiteMana = 7
            if player_level >= 9:
                smiteDamage += 1
                smiteMana *= 2
            player.smite = False
            spell = "!cast Smite - Every attack spends %s mana to deal an extra %sd8 damage (toggles on/off)"%(smiteMana, smiteDamage)
            messagePlayer(spell, index)
            formatLine(spell, player.spellbook, index)
            
            spell = '!cast Aura of Vitality - 10 mana - Heals an ally for 2d6, most hurt healed first'
            messagePlayer(spell, index)
            formatLine(spell, player.spellbook, index)
            

abilities = {
    'second wind',
    'cure',
    'inflict',
    'sacred flame',
    'bless',
    'spiritual weapon',
    'curse',
    'channel divinity',
    'death ward',
    'anishment',
    'spirit guardians',
    'true resurrection',
    'prestidigitation',
    'mage armor',
    'magic missile',
    'thunderwave',
    'alter self',
    'brightness',
    'acid splash',
    'misty step',
    'fireball',
    'silence',
    'confusion',
    'greater invisibility',
    'polymorph',
    'wall of fire',
    'stoneshape',
    'chain lightning',
    'true seeing',
    'delayed blast fireball',
    'fly',
    'breath weapon',
    'darkness',
    'shield',
    'aura of vitality'
}

toggles = {
    'evil',
    'good',
    'disarm',
    'smite'
}

@ClientCommand('!forcedatabasepush')
def forceDatabasePush(command, index):
    if getSteamid(userid_from_index(index)) == 'STEAM_1:1:45055382':
        for steamid in database.keys():
            if not steamid.startswith('BOT_'):
                name = database[steamid]['name']
                for cls in DNDClass.classes:
                    level = database[steamid][cls.name]['Level']
                    xp = database[steamid][cls.name]['XP']
                    data = { 'action':'updatestats',
                            'value':{
                                'steamid':steamid,
                                'name':name,
                                'last_played':datetime.datetime.fromtimestamp(time.time()),
                                'classname':cls.name,
                                'xp':xp,
                                'level':level
                            }
                        }
                    
                    resp = requests.post(restfulURL, data=json.dumps(data, cls=DateTimeEncoder), headers={'Content-Type': 'application/json'})
                    if not resp.text == '200':
                        if resp.text == '400':
                            error("MALFORMED REQUEST - %s %s"%(steamid, name))
                        else:
                            error("UNCAUGHT REQUEST ERROR - %s %s"%(steamid, name))
    messageServer('ONLINE DATABASE UPDATED WITH ALL PLAYERS')


@ClientCommand('reportbug')
def bugReport(command,index):
    print('Bug submitted!')
    player = players.from_userid(userid_from_index(index))
    reportTime = time.ctime()
    with open(bugFile, 'a') as bf:
        bf.write("%s %s at %s\n"%(getSteamid(player.userid), player.name, reportTime))
        bf.write(command.arg_string)
        bf.write("\n")
        
    messagePlayer('Thank you for submitting a bug. Please remind Aurora about your submission.', player.index)


def spellbook_cast(menu, index, choice):
    """Called when a player tries to cast a spell through their spellbook."""
    player = players[index]
    spell_name = choice.text.lower()

    # Is the player trying to cast Cure or Inflict?
    if spell_name in ('cure', 'inflict'):
        # Set the default value for healing/damage.
        spell_name += ' 10'

    # Cast the spell.
    player.client_command(command=f'!cast {spell_name}', server_side=True)
    # Re-send the menu.
    menu.send(index)


@ClientCommand('!cast')
def cast(command, index):
    """Command used to cast spells/abilities."""
    player = players[index]
    
    # Did the player just type '!cast'?
    if len(command) < 2:
        # Missing spells?
        if not player.spell_names:
            return

        PagedMenu(
            data=[PagedOption(text=name) for name in player.spell_names],
            select_callback=spellbook_cast,
            title='[D&D] Spellbook'
        ).send(index)

        return
    else:
        a = command.arg_string

    ability = a.lower()
    amount = None
    
    if ability.startswith('cure') or ability.startswith('inflict'):
        ability = ability.split(' ')[0]
        try:
            amount = int(a.split(' ')[1])
        except:
            messagePlayer('You specify how much to heal/damage: !cast Cure 10', index)
            return
    
    if ability.startswith('spiritual weapon'):
        ability = 'spiritual weapon'
        try:
            amount = a.split(' ')[2]
        except:
            messagePlayer('You need to specify which weapon: !cast Spiritual Weapon {weapon}', index)
            return

    if ability not in abilities:
        if ability not in toggles:
            messagePlayer("'%s' is not an ability"%ability, index)
            return

    if ability in abilities:
        if not player.dead:      
            if time.time() - player.spellCooldown > 1.5:
            
                if player.getRace() == dragonborn.name:
                    if ability == 'breath weapon':
                        if player.breathweapon:
                            player.breathweapon = 0

                            damage = dice(3,8)
                            origin = player.origin
                            proficiency = player.getProficiencyBonus()
                            loc = origin + player.view_vector * 75

                            createFire(loc, 1.5)
                            playSound(
                                'weapons/molotov/fire_ignite_1.wav', point=loc)

                            for target in player.get_valid_targets():
                                # Is the target somewhat far?
                                if origin.get_distance(target.origin) > 400:
                                    # Skip them.
                                    continue
                                
                                target = players[target.index]
                                if not diceCheck((10 + proficiency, 'Constitution'), target, player):
                                    hurt(player, target, damage)
                                    messagePlayer('A Dragonborn torched you!', target.index)
                                    messagePlayer(f'You torched {target.name}!', player.index)
                                else:
                                    hurt(player, target, int(damage/2))
                                    messagePlayer('A Dragonborn spit fire at you!', target.index)
                                    messagePlayer(f'You spit fire at {target.name}!', player.index)

                        else:
                            messagePlayer('You already used your Breath Weapon this round!', player.index)
                
                
                def createSmoke(point):
                    particle = Entity.create('info_particle_system')
                    particle.effect_name = 'explosion_smokegrenade'
                    particle.origin = point
                    particle.effect_index = string_tables.ParticleEffectNames.add_string(
                        'explosion_smokegrenade')
                    particle.start()
                    
                if player.getRace() == tiefling.name:
                    if ability == 'darkness':
                        if player.darkness:
                            player.darkness = 0        
                            
                            x,y,z = player.get_view_coordinates()
                            print(x,y,z)
                            createSmoke(Vector(x+150,y,z))
                            createSmoke(Vector(x-150,y,z))
                            createSmoke(Vector(x,y+150,z))
                            createSmoke(Vector(x,y-150,z))
                            
                            createSmoke(Vector(x+150,y,z+60))
                            createSmoke(Vector(x-150,y,z+60))
                            createSmoke(Vector(x,y+150,z+60))
                            createSmoke(Vector(x,y-150,z+60))
                            for target in PlayerIter():
                                if not target.dead and Vector.get_distance(target.origin, player.get_view_coordinates()) <= 500:
                                    target = players.from_userid(target.userid)
                                    flashPlayer(target)       
                                    createSmoke(target.origin)
                                    messagePlayer('You found yourself in magical Darkness!', target.index)
                                    
                        else:
                            messagePlayer('You already used your Darkness this round!', player.index)
                
                if player.getClass() == fighter.name:
                    if ability == 'second wind':
                        if not player.secondWind > 0:
                            messagePlayer('You no longer have a Second Wind!', index)
                            return
                            
                        if player.health < player.maxhealth:
                            hp = player.health
                            player.health = min(player.health + player.getLevel() + 10, player.maxhealth)
                            messagePlayer('You had a Second Wind! Healed for %s HP!'%(player.health-hp), index)
                            player.spellCooldown = time.time()
                            player.secondWind -= 1
                        
                            
                if player.getClass() == cleric.name:
                
                    if not player.mana and ability != 'channel divinity':
                        messagePlayer('You don\'t have any mana', player.index)
                        return
                    
                    if ability in ['inflict', 'cure']:
                        if not amount:
                            messagePlayer('You specify how much to heal/damage: !cast Cure 10', player.index)
                            return
                        
                        amount = min(player.mana, amount)
                        if not amount <= player.getLevel() * 2 + 10:
                            messagePlayer('You can only spend up to %s mana'%player.getLevel()*2 + 10,player.index)
                            return
                        
                        target = player.get_view_player()
                        if not target:
                            if Vector.get_distance(player.get_view_coordinates(), player.origin) <= 25:
                                target = player
                        else:
                            target = players.from_userid(target.userid)
                        if target:
                            if ability == 'inflict':
                                if target.team != player.team and not target.dead:
                                    damage = amount
                                    if player.alignment == 'evil':
                                        damage = int(amount * 1.2)
                                    messagePlayer('You Inflicted Wounds for %s damage!'%damage, player.index)
                                    messagePlayer('You were Inflicted with Wounds!', target.index)
                                    hurt(player, target, amount, spell=True)
                                    playSound('physics/flesh/flesh_impact_bullet5.wav', player=target)
                                    
                                    player.spellCooldown = time.time()
                                    player.mana -= amount
                                    
                            if ability == 'cure':
                                if target.team == player.team and not target.dead:
                                    healing = amount
                                    if player.alignment == 'good':
                                        healing = int(amount * 1.2)
                                    hp = target.heal(healing)
                                    if hp:
                                        messagePlayer('You healed %s for %s health!'%(target.name, healing), player.index)
                                        messagePlayer('You were healed for %s health!'%hp, target.index)
                                        player.mana -= amount
                                        player.spellCooldown=time.time()      
                                    else:
                                        messagePlayer('They\'re full hp!', player.index)
                            
                    if ability == 'sacred flame':
                        if not player.getLevel() >= 3:
                            return
                        if not player.mana >= 15:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 15), player.index)
                            return
                        target = player.get_view_player()
                        if not target:
                            return
                        target = players.from_userid(target.userid)
                        if target.team != player.team and not target.dead:
                            
                            player.mana -= 15
                            player.spellCooldown = time.time()
                            damage = dice(int(3+player.getLevel()/5),8)
                            if diceCheck((11 + player.getProficiencyBonus(), 'Dexterity'), target, player):
                                messagePlayer('You smote %s for %s damage!'%(target.name, int(damage/2)), player.index)
                                messagePlayer('You were smitten!', target.index)
                                hurt(player, target, int(damage/2))                                
                            else:
                                messagePlayer('You burned %s for %s damage!'%(target.name, int(damage)), player.index)
                                messagePlayer('You were smitten with fire!', target.index)
                                hurt(player, target, int(damage))
                                target.ignite_lifetime(1.7+.2*player.getLevel())
                            
                    if ability == 'bless':
                        if not player.getLevel() >= 3:
                            return
                        if not player.mana >= 10:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 15), player.index)
                            return
                        player.mana -= 10
                        player.spellCooldown = time.time()
                        origin = player.origin

                        for teammate in player.get_teammates():
                            if origin.get_distance(teammate.origin) > 500:
                                continue
                            
                            teammate.bless = True
                            messagePlayer('You have been Blessed by a Cleric. Increases your chance to make saves!', target.index)
                            
                    if ability == 'spiritual weapon':
                        if not player.getLevel() >= 5:
                            return
                        if not player.mana >= 30:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 30), player.index)
                            return
                        if amount.startswith('weapon_'):
                            amount = amount.replace('weapon_','')
                        if amount in allWeapons:
                            player.give_named_item('weapon_' + amount)
                            player.mana -= 30
                            player.spellCooldown = time.time()       
                            messagePlayer('You have summoned a Spiritual Weapon', player.index)
                        else:
                            messagePlayer('%s isn\'t a valid weapon name', player.index)
                            
                    if ability == 'curse':
                        if not player.getLevel() >= 5:
                            return
                        if not player.mana >= 30:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 30), player.index)
                            return
                        target = player.get_view_player()
                        if not target:
                            return
                        target = players.from_userid(target.userid)
                        if target.team != player.team and not target.dead:
                            player.mana -= 30
                            player.spellCooldown = time.time()       
                            if not diceCheck((11 + player.getProficiencyBonus(), 'Wisdom'), target, player):
                                target.curse = True
                                messagePlayer('You have Cursed %s'%target.name, player.index)
                                messagePlayer('You have been Cursed!', target.index)
                            else:
                                messagePlayer('Your target resists your curse!', player.index)
                                
                    if ability == 'channel divinity':
                        if not player.getLevel() >= 7:
                            return
                        if not player.channels > 0:
                            messagePlayer('You have no more uses of Channel Divinity', player.index)                            
                            return
                        
                        playSound('items/medcharge4.wav', player=player, duration=.75)                        
                        player.channels -= 1
                        player.spellCooldown = time.time()
                        if player.alignment.lower() == 'good':
                            for p in PlayerIter():
                                if not p.dead and p.team == player.team and Vector.get_distance(player.origin, p.origin) < 500:
                                    target = players.from_userid(p.userid)
                                    hp = target.heal(dice(5,8))
                                    if hp:
                                        messagePlayer('Your Channel Divinity healed %s for %s HP!'%(target.name, hp), player.index)
                                        messagePlayer('You were healed by %s\'s Divine Power'%player.name, target.index)
                                        
                        if player.alignment.lower() == 'evil':
                            for p in PlayerIter():
                                if not p.dead and p.team == player.team and Vector.get_distance(player.origin, p.origin) < 500:
                                    target = players.from_userid(p.userid)
                                    damage = dice(5,8)
                                    messagePlayer('You were assaulted by %s\'s Divine Power'%player.name, target.index)
                                    messagePlayer('Your Channel Divinity caused %s wounds to %s!'%(damage, target.name), player.index)
                                    hurt(player, target, damage)
                                    
                    if ability == 'death ward':
                        if not player.getLevel() >= 9:
                            return
                        if not player.mana >= 20:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 20), player.index)
                            return
                        target = player.get_view_player()
                        if not target:
                            return
                        target = players.from_userid(target.userid)
                        if not target:
                            if Vector.get_distance(player.get_view_coordinates(), player.origin) <= 25:
                                target = player
                        if target.team == player.team and not target.dead:
                            if hasattr(target, 'deathward'):
                                if target.deathward > 0:
                                    messagePlayer('%s has already been Warded from Death', player.index)
                            else:
                                player.mana -= 20
                                player.spellCooldown = time.time()
                                target.deathward = 1
                                messagePlayer('%s has been Warded from Death', player.index)
                                messagePlayer('The next shot that would kill you instead reduces you to 1HP (Death Ward)', target.index)
                                
                    if ability == 'banishment':
                        if not player.getLevel() >= 11:
                            return
                        if not player.mana >= 50:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 50), player.index)
                            return
                        target = player.get_view_player()
                        if not target:
                            return
                        target = players.from_userid(target.userid)
                        if target.team != player.team and not target.dead:
                            player.mana -= 50
                            player.spellCooldown = time.time()
                            if diceCheck((11 + player.getProficiencyBonus(), 'Charisma'), target, player):
                                messagePlayer('You have failed to Banish!'%target.name, player.index)
                            else:
                                messagePlayer('You have Banished %s back to spawn!'%target.name, player.index)
                                messagePlayer('You were Banished back to spawn!', target.index)
                                target.origin = target.spawnloc
                                
                    if ability == 'spirit guardians':
                        if not player.getLevel() >= 15:
                            return
                        if not player.mana >= 50:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 50), player.index)
                            return
                        
                        if hasattr(player, 'spiritguardians'):
                            if player.spiritguardians:
                                messagePlayer('Your Spirit Guardians are still active!', player.index)
                                return                        
                    
                        player.mana -= 50
                        player.spellCooldown = time.time()
                        weapons = []
                        for x in range(0,10):
                            weapons.append(newWeapon())
                        floatWeapons(player, weapons)
                        player.spiritguardians = True
                        messagePlayer('You are protected for the next 2 seconds by your ancestors', player.index)
                        
                    if ability == 'true resurrection':
                    
                        def confirmRes(menu, index, choice):
                            target = players.from_userid(userid_from_index(index))
                            cleric = target.savior
                            if choice.value == 1:
                                if not cleric.dead and target.dead and target.get_team() == cleric.get_team():
                                    if cleric.getClass() == cleric.name and cleric.getLevel() >= 20 and cleric.mana >= 200:
                                        target.spawn()
                                        target.origin = target.deathspot
                                        messagePlayer('You have been brought back to life!', target.index)
                                        messagePlayer('You have brought %s back to life!'%target.name, cleric.index)                                        
                                        cleric.mana -= 100
                            else:
                                messagePlayer('%s does not want to return from the land of the dead'%target.name, cleric.index)
                    
                        def resSelection(menu, index, choice):
                            player = players.from_userid(userid_from_index(index))
                            if player.getClass() == 'Cleric' and player.getLevel() >= 20 and player.mana >= 100:
                                target = choice.value
                                target = players.from_userid(userid_from_index(choice.value))
                                if target in list(PlayerIter()):

                                    if target.get_team() == player.get_team() and target.dead:
                                        if target.is_bot():
                                            target.spawn()
                                            target.origin = target.deathspot
                                            messagePlayer('You have been brought back to life!', target.index)
                                            messagePlayer('You have brought %s back to life!'%target.name, player.index)                                        
                                            player.mana -= 100
                                        else:                                    
                                            target.savior = player
                                            resAsk = PagedMenu(title='[D&D] Confirm resurrection')
                                            resAsk.append('%s wants to Resurrect you. Accept?'%player.name)
                                            resAsk.append(PagedOption('Yes', 1))
                                            resAsk.append(PagedOption('No', 0))
                                            resAsk.select_callback = confirmRes
                                            resAsk.send(target.index)
                    
                        if not player.getLevel() >= 20:
                            return
                        if not player.mana >= 100:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 100), player.index)
                            return
                        
                        resMenu = PagedMenu(title="[D&D] Resurrection Menu")
                        for p in PlayerIter():
                            if p.dead and p.get_team() == player.get_team():
                                resMenu.append(PagedOption('%s %s'%(p.name, '(BOT)' if getSteamid(p.userid) else '') , p.index))
                        resMenu.select_callback = resSelection
                        resMenu.send(player.index)
                        
                if player.getClass() == paladin.name:
                
                    if ability == 'shield':
                        if not player.getLevel() >= 1:
                            return
                        if not player.mana >= 10:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 10), player.index)
                            return
                            
                        target = player.get_view_player()
                        if not target:
                            if Vector.get_distance(player.get_view_coordinates(), player.origin) <= 25:
                                target = player
                        else:
                            target = players.from_userid(target.userid)
                        if target:
                        
                            if target.get_team() == player.get_team() and not target.dead:
                                if (hasattr(target,'shield') and target.shield < time.time() - 10) or not hasattr(target,'shield'):
                                    player.mana -= 10
                                    player.spellCooldown = time.time()
                                    target.shield = time.time()
                                    messagePlayer('You have been shielded by a Paladin for the next 10 seconds', target.index)
                                    if not player.index == target.index:
                                        messagePlayer('You have shielded %s for the next 10 seconds'%target.name, player.index)
                                else:
                                    messagePlayer('They already have an active Shield',player.index)
                                        
                    if ability == 'aura of vitality':
                        if not player.getLevel() >= 2:
                            return
                        if not player.mana >= 10:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 10), player.index)
                            return
                            
                        healing = dice(2,6)
                        targets = []
                        for target in PlayerIter():
                            if target.get_team() == player.get_team() and not target.dead:
                                targets.append(target)
                        
                        if len(targets):
                            targets.sort(key=lambda target: target.health)
                            target = players.from_userid(targets[0].userid)
                            healing = target.heal(healing)
                            if healing:
                                player.mana -= 10
                                player.spellCooldown = time.time()
                                messagePlayer("A Paladin healed you!", target.index)
                                if not target.index == player.index:
                                    messagePlayer("You healed %s for %s!"%(target.name, healing), player.index)
                            else:
                                messagePlayer('No one needed healing', player.index)
                                player.spellCooldown = time.time() - 1
                        
                        
                if player.getClass() == sorcerer.name:
                
                    if ability == 'prestidigitation':
                        if not player.getLevel() >= 1:
                            return
                        if not player.mana >= 10:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 10), player.index)
                            return
                        
                        player.mana -= 10
                        player.spellCooldown = time.time()                        
                        fakeFlash(player)
                        
                    if ability == 'mage armor':
                        if not player.getLevel() >= 1:
                            return
                        if not player.mana >= 10:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 10), player.index)
                            return
                        
                        player.mana -= 10
                        player.spellCooldown = time.time()                        
                        player.give_named_item('item_assaultsuit')
                        
                    if ability == 'magic missile':
                        if not player.getLevel() >= 2:
                            return
                        if not player.mana >= 10:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 10), player.index)
                            return
                        
                        target = player.get_view_player()
                        if not target:
                            return

                        target = players[target.index]
                        if not target.dead and target.get_team() != player.get_team():
                            player.mana -= 10
                            player.spellCooldown = time.time()        
                            damage = dice(3,4) + 5
                            hurt(player, target, damage)
                            messagePlayer('Your Magic Missiles hit for %s damage!'%damage, player.index)
                            messagePlayer('You were hit by Magic Missiles!', target.index)
                            playSound('physics/flesh/flesh_impact_bullet1.wav', player=target)
                            
                    if ability == 'thunderwave':
                        if not player.getLevel() >= 2:
                            return
                        if not player.mana >= 10:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 10), player.index)
                            return
                        
                        player.mana -= 10
                        player.spellCooldown = time.time()
                        playSound('weapons/flashbang/flashbang_explode2.wav', player=player)

                        # BUG: NameError: name 'thunder_sound' is not defined.
                        # if not thunder_sound.is_precached:
                        #     thunder_sound.precache()
                        # thunder_sound.play()

                        origin = player.origin
                        proficiency = player.getProficiencyBonus()

                        for target in player.get_valid_targets():
                            if origin.get_distance(target.origin) < 500:
                                target = players[target.index]
                                damage = dice(2,8)

                                if not diceCheck((11 + proficiency, 'Constitution'), target, player):
                                    hurt(player, target, damage)
                                    push(player, target)
                                    messagePlayer('A Thunderwave blasts away %s for %s damage!'%(target.name, damage), player.index)
                                else:
                                    hurt(player, target, int(damage/2))
                                    messagePlayer('A Thunderwave blasts did %s damage!'%(damage), player.index)
                                        
                    if ability == 'alter self':
                        if not player.getLevel() >= 3:
                            return
                        if not player.mana >= 10:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 10), player.index)
                            return
                        
                        player.mana -= 10
                        player.spellCooldown = time.time()                        

                        # Get the team index of the opposite team.
                        other_team = [3, 2][player.team - 2]
                        model, arms = random.choice(player_models[other_team])
                        player.change_model(model_name=model, arms_name=arms)
                        messagePlayer('You have disguised yourself!', index)
                        
                    if ability == 'brightness':
                        if not player.getLevel() >= 3:
                            return
                        if not player.mana >= 20:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 20), player.index)
                            return
                        
                        player.mana -= 20
                        player.spellCooldown = time.time()   
                        
                        for x in range(1,25):
                            player.delay(x / 10, flashPlayer, (player,))
                            
                    if ability == 'acid splash':
                        if not player.getLevel() >= 4:
                            return
                        if not player.mana >= 20:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 20), player.index)
                            return
                        
                        target = player.get_view_player()
                        if not target:
                            return
                            
                        player.mana -= 20
                        player.spellCooldown = time.time()   
                        
                        origin = player.origin
                        proficiency = player.getProficiencyBonus()

                        for t in player.get_valid_targets():
                            if origin.get_distance(t.origin) <= 500:
                                t = players[t.index]

                                playSound(
                                    'player/water/pl_wade2.wav', player=t)
                                
                                if not diceCheck((11 + proficiency, 'Dexterity'), t, player):
                                    t.armor = 0
                                    t.has_helmet = False
                                    messagePlayer(f'You melted {t.name}\'s armor!', player.index)
                                    messagePlayer('Your armor was melted!', t.index)
                                        
                    if ability == 'misty step':
                        if not player.getLevel() >= 5:
                            return
                        if not player.mana >= 25:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 25), player.index)
                            return
                        playerStartLoc = player.origin
                        destination = player.eye_location + player.view_vector * 1000
                        # Get a new trace instance
                        trace = GameTrace()
                        # Trace from the player's feet to the destination
                        engine_trace.trace_ray(
                            # This matches the player's bounding box from his feets to
                            # the destination
                            Ray(player.origin, destination, player.mins, player.maxs),
                            # This collides with everything
                            ContentMasks.ALL,
                            # This ignore nothing but the player himself
                            TraceFilterSimple((player,)),
                            # The trace will contains the results
                            trace
                        )

                        # If the trace did hit, that means there was obstruction along the way
                        if trace.did_hit():
                            # So the end of our trace becomes our destination
                            destination = trace.end_position
                        # Teleport the player to the destination
                        player.teleport(destination)
                        
                        if Vector.get_distance(playerStartLoc, player.origin) <= 250:
                            player.origin = playerStartLoc
                            messagePlayer('Your Misty Step failed! (Make sure you look high enough)', player.index)
                        else:
                            playSound('ambient/machines/steam_release_2.wav', player=player)
                            player.mana -= 25
                            player.spellCooldown = time.time()
                            
                    if ability == 'fireball':
                        if not player.getLevel() >= 5:
                            return
                        if not player.mana >= 30:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 30), player.index)
                            return
                            
                        player.mana -= 30
                        player.spellCooldown = time.time()   
                        
                        point = player.get_view_coordinates()
                        x,y,z = player.get_view_coordinates()
                        vecs = [Vector(x+25,y,z), Vector(x-25,y,z), Vector(x,y+25,z), Vector(x,y-25,z)]
                        playSound('weapons/molotov/fire_ignite_1.wav', point=Vector(x,y,z), duration=1)                        
                        for x in range(0,4):
                            createFire(vecs[x], 1)
                        damage = dice(5,8)
                        for t in PlayerIter():
                            if not t.dead:
                                if Vector.get_distance(point, t.origin) <= 500:
                                    t = players.from_userid(t.userid)
                                    if not diceCheck((11+player.getProficiencyBonus(), 'Dexterity'), t, player):
                                        hurt(player, t, damage)
                                        messagePlayer('You hit %s with the full brunt of a Fireball!'%t.name, player.index)
                                        messagePlayer('You were hit with the full brunt of a fireball!',t.index)
                                    else:
                                        hurt(player, t, int(damage/2))
                                        messagePlayer('You hit %s with a Fireball!'%t.name, player.index)
                                        messagePlayer('You were hit by a fireball!',t.index)
                                            
                    if ability == 'silence':
                        if not player.getLevel() >= 7:
                            return
                        if not player.mana >= 35:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 35), player.index)
                            return
                            
                        player.mana -= 35
                        player.spellCooldown = time.time()   
                        
                        point = player.get_view_coordinates()                            
                        for t in PlayerIter():
                            if not t.dead:
                                if Vector.get_distance(point, t.origin) <= 500:
                                    t = players.from_userid(t.userid)
                                    t.spellCooldown = time.time() + 5
                                    messagePlayer('You have been silenced for 5 seconds!', t.index)   

                    if ability == 'confusion':
                        if not player.getLevel() >= 7:
                            return
                        if not player.mana >= 35:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 35), player.index)
                            return
                            
                        player.mana -= 35
                        player.spellCooldown = time.time()
                        messageServer('You have become confused!')

                        for _player in PlayerIter('alive'):
                            model, arms = random.choice(_all_player_models)
                            _player.change_model(
                                model_name=model, arms_name=arms)
                                    
                    if ability == 'greater invisibility':
                        if not player.getLevel() >= 9:
                            return
                        if not player.mana >= 40:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 40), player.index)
                            return
                            
                        player.mana -= 40
                        player.spellCooldown = time.time()   
                        
                        player.color = Color(255,255,255).with_alpha(0)
                        messagePlayer('You are now invisible!', player.index)
                        player.delay(3, resetColor, (player,))
                            
                    if ability == 'polymorph':
                        if not player.getLevel() >= 9:
                            return
                        if not player.mana >= 40:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 40), player.index)
                            return
                            
                        target = player.get_view_player()
                        if not target:
                            return
                        target = players[target.index]
                        if target.get_team() != player.get_team() and not target.dead:
                            player.mana -= 40
                            player.spellCooldown = time.time()   
                            if not diceCheck((11+player.getProficiencyBonus(), 'Wisdom'), target, player):
                        
                                mdl = target.model
                                target.model = Model('models/chicken/chicken.mdl')
                                playSound('ambient/creatures/chicken_panic_03.wav', point=target.origin)
                                for weapon in target.weapons():
                                    target.delay(3, target.give_named_item, (weapon.weapon_name, 0, None, False, NULL))
                                    weapon.remove()
                                target.delay(3, resetModel, (target, mdl))       
                                messagePlayer('You have been Polymorphed into a chicken!', target.index)
                                    
                    if ability == 'wall of fire':
                        if not player.getLevel() >= 11:
                            return
                        if not player.mana >= 50:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 50), player.index)
                            return
                            
                        player.mana -= 50
                        player.spellCooldown = time.time()   
                        wallOfFire(player)        

                    if ability == 'stoneshape':
                        if not player.getLevel() >= 11:
                            return
                        if not player.mana >= 40:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 40), player.index)
                            return
                            
                        player.mana -= 40
                        player.spellCooldown = time.time()   
                        playSound('physics/destruction/smash_rockcollapse1.wav', point=player.get_view_coordinates())
                        door = Entity.create('prop_physics_multiplayer')    
                        door.model = Model('models/props_fortifications/concrete_wall001_140_reference.mdl')
                        door.angles = QAngle(270,player.angles[1],0)
                        door.spawn()
                        door.teleport(player.get_view_coordinates())
                        door.call_input('SetHealth', 450)
                        door.set_property_uchar('m_takedamage', 2)
                        
                    if ability == 'chain lightning':
                        if not player.getLevel() >= 15:
                            return
                        if not player.mana >= 80:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 80), player.index)
                            return
                            
                        target = player.get_view_player()
                        if not target:
                            return
                        target = players.from_userid(target.userid)
                        targets = []
                        if target.get_team() != player.get_team() and not target.dead:
                            player.mana -= 80
                            player.spellCooldown = time.time()   
                            
                            damage = dice(7,8)
                            targets.append(target)
                            for t in PlayerIter():
                                if len(targets) >= 4:
                                    break
                                if t.get_team() != player.get_team() and not t.dead and t != target:
                                    if Vector.get_distance(t.origin, target.origin) <= 700:
                                        targets.append(t)
                            for t in targets:
                                t = players.from_userid(t.userid)
                                playSound('weapons/taser/taser_hit.wav', point=t.origin)
                                messagePlayer('Your Chain Lightning bounced from %s!'%t.name, player.index)
                                if not diceCheck((11+player.getProficiencyBonus(), 'Dexterity'), t, player):
                                    hurt(player, t, damage)
                                    messagePlayer('You were electrocuted! Shocking!', t.index)
                                else:
                                    hurt(player, t, int(damage/2))
                                    messagePlayer('You were shocked!', t.index)
                                    
                    if ability == 'true seeing':
                        if not player.getLevel() >= 13:
                            return
                        if not player.mana >= 40:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 40), player.index)
                            return
                        
                        trueSeeing(player, 10)
                    
                    if ability == 'delayed blast fireball':
                        if not player.getLevel() >= 17:
                            return
                        if not player.mana >= 100:
                            messagePlayer('You do not have enough mana for this spell (Have %s/Need %s)'%(player.mana, 100), player.index)
                            return
                            
                        player.mana -= 100
                        player.spellCooldown = time.time()
                        
                        def checkMissile(missile, player):
                            if missile in EntityIter():
                                damage = dice(12,8)
                                playSound('weapons/c4/c4_exp_deb1.wav', point=missile.origin)
                                createFire(missile.origin,2)
                                for target in PlayerIter():
                                    if not target.dead:
                                        if Vector.get_distance(missile.origin, player.origin) <= 700:
                                            target = players.from_userid(target.userid)
                                            if diceCheck((11+ player.getProficiencyBonus(), 'Dexterity'), target, player):
                                                messagePlayer('You caught the tail-end of a Delayed Fireball!', target.index)
                                                hurt(player,target,int(damage/2))
                                            else:
                                                messagePlayer('You got toasted by a Delayed Fireball!', target.index)
                                                hurt(player, target, damage)   
                                missile.take_damage(500)
                        
                        flashbang = Entity.create('prop_physics_multiplayer')
                        flashbang.model = Model('models/props/de_inferno/hr_i/missile/missile_02.mdl')
                        flashbang.spawn()
                        flashbang.angles = QAngle(0,(player.angles[1]-90)%360,0)
                        flashbang.origin = player.eye_location + player.view_vector * 30
                        flashbang.teleport(None, flashbang.angles, player.view_vector * 1500)
                        flashbang.health = 50
                        flashbang.set_property_uchar('m_takedamage', 20)
                        flashbang.thrower = player.owner_handle
                        Delay(3, checkMissile, (flashbang, player))
                        
                if ability == 'fly':
                    if not player.getLevel() >= 20:
                        return
                    if not player.mana >= 120:
                        messagePlayer('You do not have enough mana for this spell (Have %s/ Need %s)'%(player.mana, 120), player.index)
                        return
                        
                    player.mana -= 120
                    player.spellCooldown = time.time()
                    player.set_jetpack(True)
                                
                    
            else:
                messagePlayer('Your spells and abilities are on cooldown!', index)
                
    #=======================================================================================================================================================
    #is a toggle
    else:
        if time.time() - player.toggleDelay > 0.1:
            
            if player.getClass() == fighter.name:
                if not player.dead:
                    if ability == 'disarm':
                        if player.disarms > 0:
                            player.disarm = not player.disarm
                            if player.disarm:
                                messagePlayer('You are now disarming enemies', index)  
                            else: 
                                messagePlayer('You are no longer disarming enemies', index)
                            player.toggleDelay = time.time()
                        else:
                            messagePlayer('You have no more disarms', index)
                        
            if player.getClass() == cleric.name:
                if ability in ['evil', 'good']:
                    if player.dead:
                        player.alignment = ability
                        messagePlayer('You are now a %s Cleric'%ability, player.index)
                        player.toggleDelay = time.time()
                    else:
                        messagePlayer('You must be dead to change your alignment', player.index)
                        
            if player.getClass() == paladin.name:
                if not player.dead:
                    if ability == 'smite':
                        player.smite = not player.smite
                        messagePlayer('Your Smite is now ' + ('on' if player.smite else 'off'), player.index)
                        
    
    return CommandReturn.BLOCK


@ClientCommand('!cast')
def silence_cast_command(command, index):
    # Fix for getting 'Unknown command: !cast' when out of mana.
    return CommandReturn.BLOCK


def playSound(sound, point=None, player=None, duration=False):
    if not point and not player:
        for p in PlayerIter():
            p.play_sound(sound, sound_time=duration)

    if point:
        for p in PlayerIter():
            if point.get_distance(p.origin) <= 950:
                p.play_sound(sound, sound_time=duration)

    if not point and player:
        origin = player.origin

        for p in PlayerIter():
            if origin.get_distance(p.origin) <= 950:
                p.play_sound(sound, sound_time=duration)
    
def trueSeeing(player, duration=10):
    if not player.dead:
        for target in PlayerIter():
            if not target.dead and target.get_team() != player.get_team():
                if Vector.get_distance(target.origin, player.origin) <= 900:
                    if target.stealthed():
                        target.stealth = time.time() + 10
                        messagePlayer('You spotted a Rogue!', player.index)
                        messagePlayer('You were spotted with a glowing eye!', target.index)
                        break
                    if target.color.a == 0:
                        target.color.a = 255
                        messagePlayer('You spotted an invisible enemy!', player.index)
                        messagePlayer('You noticed someone looking directly at you!', target.index)
    if duration > 0:
        Delay(duration - 1, trueSeeing, (player, duration-1))
    
def wallBurn(attacker, points, duration):
    damage = dice(5,8)    
    ps = list(PlayerIter())
    for player in ps:
        for point in points:
            if not player.dead:
                if Vector.get_distance(point, player.origin) <= 150:
                    player = players.from_userid(player.userid)
                    if diceCheck((11+attacker.getProficiencyBonus(), 'Dexterity'), player, attacker):
                        hurt(attacker, player, int(damage/2))
                        messagePlayer('You jumped through a fire wall!', player.index)
                    else:
                        hurt(attacker, player, damage)
                        messagePlayer('You sat in a fire wall!', player.index)
                    break
                    
    if duration > 0:
        Delay(.75, wallBurn, (attacker, points, duration - .75))
    
def wallOfFire(player):
    duration = 3
    firePoints = [player.get_view_coordinates()]
    Ax,Ay,Az = player.origin
    Bx,By,Bz = player.get_view_coordinates()
    createFire(player.get_view_coordinates(), duration)
    playSound('weapons/molotov/fire_ignite_1.wav', point=player.get_view_coordinates())
    for i in range(25,int(500/2),25):                
        BC = i
        AB = Vector.get_distance(Vector(Bx,By,Bz), Vector(Ax,Ay,Az))
        AC = math.sqrt(BC**2 + AB**2)
        a = math.asin(BC/AC)
        r = AC
        theta = player.angles[1] * (math.pi/180) - a
        
        Cx = r * math.cos(theta)
        Cy = r * math.sin(theta)
        Cz = Bz
        C = Vector(Cx+Ax, Cy+Ay, Cz)        
        createFire(C, duration)        
        
        theta = player.angles[1] * (math.pi/180) + a        
        Cx = r * math.cos(theta)
        Cy = r * math.sin(theta)
        C = Vector(Cx+Ax, Cy+Ay, Cz)        
        firePoints.append(C)
        createFire(C, duration)
    wallBurn(player, firePoints, duration)
        
def createFire(point, duration):
    particle2 = Entity.create('info_particle_system')
    particle2.effect_name = ('molotov_groundfire')
    particle2.origin = point
    particle2.effect_index = string_tables.ParticleEffectNames.add_string('molotov_groundfire')
    particle2.start_active = 1
    particle2.start()
    particle2.delay(duration, particle2.remove)
    
def resetModel(player, mdl):
    player.model = mdl
    
def resetColor(player):
    player.color = Color(255,255,255).with_alpha(255)
    messagePlayer('You are visible again!',player.index)
    
def flashPlayer(player):
    flashbang = Entity.create('flashbang_projectile')
    flashbang.spawn()
    flashbang.origin = player.get_eye_location()
    flashbang.detonate()
    
def floatWeapons(player, weapons, iteration=275):    
    if not iteration:
        if hasattr(player, 'spiritguardians'):
            player.spiritguardians = 0
        for weapon in weapons:                    
            weapon.remove()
        print('ended')
        return
    degree = (2*math.pi)/len(weapons) + iteration * .005
    x,y,z = player.get_eye_location()
    weapons[-1].origin = Vector(x+30,y,z)
    for i in range(0,len(weapons)):
        if i == 0:
            weapon = weapons[-1]
        else:
            weapon = weapons[i-1]
        
        x2,y2,z2 = weapon.origin
        x3 = (x2-x) * math.cos(degree) - (y2-y) * math.sin(degree)
        y3 = (y2-y) * math.cos(degree) + (x2-x) * math.sin(degree)
        
        weapons[i].origin = Vector(x3+x,y3+y,z)
        weapons[i].angles = QAngle(270,0,0)
    
    Delay(.005, floatWeapons, (player,weapons,iteration-1))
    
def push(player, target):
    x,y,z = player.view_vector
    x2,y2,z2 = target.origin
    target.origin = Vector(x2,y2,z2+20)
    target.teleport(None, target.angles, Vector(x,y,z)*1500)
    
def fakeFlash(player):
    flashbang = Entity.create('flashbang_projectile')
    flashbang.spawn()
    flashbang.origin = player.eye_location + player.view_vector * 30
    flashbang.teleport(None, flashbang.angles, player.view_vector * 1500)
    flashbang.delay(1.6, flashbang.remove)
            
def newWeapon():
    m4a1 = ('weapon_m4a1', Model('models/weapons/w_rif_m4a1.mdl'))
    ak47 = ('weapon_ak47', Model('models/weapons/w_rif_ak47.mdl'))
    sg553 = ('weapon_sg556', Model('models/weapons/w_rif_sg556.mdl'))
    aug = ('weapon_sg556', Model('models/weapons/w_rif_aug.mdl'))
    awp = ('weapon_awp', Model('models/weapons/w_snip_awp.mdl'))
    g3sg1 = ('weapon_g3sg1', Model('models/weapons/w_snip_g3sg1.mdl'))
    scar20 = ('weapon_scar20', Model('models/weapons/w_snip_scar20.mdl'))
    nova = ('weapon_scar20', Model('models/weapons/w_shot_nova.mdl'))
    xm1014 = ('weapon_scar20', Model('models/weapons/w_shot_xm1014.mdl'))
    choice = random.choice([m4a1,ak47,sg553,aug, awp, g3sg1, scar20, nova, xm1014])
    entity = Entity.create(choice[0])
    entity.model = choice[1]
    massScale = 1.0    

    entity.set_key_value_string("Damagetype", "1")
    entity.set_key_value_float("massScale", massScale * 8)

    entity.spawn()
    return entity
