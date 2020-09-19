from messages import SayText2
from pprint import pprint
from events import Event
from events.hooks import PreEvent
from players.helpers import userid_from_index
from players.helpers import index_from_userid
from players.helpers import uniqueid_from_index
from players.constants import PlayerButtons
from players.entity import Player
from players.dictionary import PlayerDictionary
from entities.entity import Entity
from entities.entity import BaseEntity
from entities.hooks import EntityCondition, EntityPreHook
from entities import TakeDamageInfo
from entities.helpers import index_from_inthandle
from entities.helpers import index_from_basehandle
from mathlib import Vector
from mathlib import NULL_VECTOR
from filters.entities import EntityIter
from filters.players import PlayerIter
from filters.recipients import RecipientFilter
from memory import make_object
from memory.hooks import PreHook
from os.path import join, dirname, abspath
from listeners import OnPlayerRunCommand
from listeners.tick import Delay
from weapons.dictionary import WeaponDictionary
from weapons.entity import Weapon
from engines.server import global_vars
from effects.base import TempEntity
from colors import Color
from plugins.manager import plugin_manager
from menus import SimpleMenu
from menus import Text
from menus import PagedMenu
from menus import PagedOption
from commands.client import ClientCommand
from commands import CommandReturn
from itertools import chain 
import math
import random
import os
import sys
import shutil
import json
import time

database = {}
databaseLocation = join(dirname(__file__), "dnd5e.db")
webDatabase = ''
sourceFiles = ''
release = ''
debugValue = True
###############################################################
# XP Values
killXP = 10
headshotXP = 14
plantBombXP = 30
defuseBombXP = 50
explodedBombXP = 50
roundWinXP = 50
rescueXP = 10
humanXP = 1.1
###############################################################
cterrorists = 2
terrorists = 3

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

def dice(number, sides):
    total = 0
    for die in range(1,number+1):
        total += random.randint(1,sides)
    return total

def diceCheck(check, player):
    #Check should be a tuple of (Int, Str)
    #                           Save, Type
    
    bonus = 0
    if hasattr(player, 'bless'):
        if player.bless:
            bonus += dice(1,4)
    
    if check[1] in player.getSaves():
        result = random.randint(1,20) + (self.getLevel() - 1) / 4 + 2 + bonus > check[0]        
        if hasattr(player, 'indomitable'):
            if not result and player.indomitable > 1:
                player.indomitable -= 1
                return random.randint(1,20) + (self.getLevel() - 1) / 4 + 2 + bonus > check[0]
        return result
        
    result = random.randint(1,20) + bonus > check[0]
    if hasattr(player, 'indomitable'):
        if not result and player.indomitable > 1:
            player.indomitable -= 1
            return random.randint(1,20) + bonus > check[0]
    return result


class DNDClass():
    
    classes = []
    defaultClass = None
    
    def __init__(self, name, description=None, requiredClasses=None, defaultClass=False, save=None, weapons=[]):
            
        self.name = name
        #self.requiredClasses = {fighter: 3, cleric: 3}
        self.requiredClasses = requiredClasses
        self.description = description
        self.save = save
        self.weapons = weapons
        DNDClass.classes.append(self)
        if defaultClass:
            if not DNDClass.defaultClass:
                DNDClass.defaultClass = self

cleric = DNDClass('Cleric', 'A priest who follows a path of good or evil. Uses divine power to fight.', save='Wisdom')       
cleric.weapons = list(chain(knife, pistols, heavypistols, taser, shotguns, lmg, smg))
cleric.weaponDesc = ['Pistols', 'Heavy Pistols', 'Taser', 'Shotguns', 'LMGs', 'SMGs']

fighter = DNDClass('Fighter', 'Uses martial prowess and tactical maneuvers to defeat enemies.', defaultClass=True, save='Fortitude')
fighter.weapons = list(chain(knife, pistols, heavypistols, shotguns, lmg, smg, rifles, bigsnipers, {'hegrenade'}))
fighter.weaponDesc = ['HE Grenade', 'Pistols', 'Heavy Pistols', 'Shotguns', 'LMGs', 'SMGs', 'Rifles', 'AWP', 'Autosnipers']

rogue = DNDClass('Rogue', 'Strikes from the shadows and uses guile to outmaneuver enemies.', save='Dexterity')
rogue.weapons = list(chain(knife, pistols, heavypistols, shotguns, smg, {'ssg08'}, grenades))
rogue.weaponDesc = ['Pistols', 'Heavy Pistols', 'Shotguns', 'SMGs', 'Scout', 'Grenades', 'Taser']

sorcerer = DNDClass('Sorcerer', 'Descended from a magical blood line, their magic is innate and awe-inspiring.', save='Constitution')
sorcerer.weapons = list(chain(knife, pistols, grenades))
sorcerer.weaponDesc = ['Pistols', 'Grenades', 'Taser']

monk = DNDClass('Monk', 'Disciplined. Quick. Mind and body. A master of both.', requiredClasses={fighter:7, rogue:7}, save=['Strength', 'Dexterity'])
monk.weapons = list(chain(knife, pistols, heavypistols, smg))
monk.weaponDesc = ['Pistols', 'Heavy Pistols', 'SMGs']

paladin = DNDClass('Paladin', 'A holy crusader who has taken an oath to serve a higher calling.', requiredClasses={fighter:7,cleric:7}, save=['Wisdom', 'Charisma'])
paladin.weapons = list(chain(knife, pistols, heavypistols, shotguns, lmg, smg, rifles, bigsnipers, {'hegrenade'}))
paladin.weaponDesc = ['HE Grenade', 'Pistols', 'Heavy Pistols', 'Shotguns', 'LMGs', 'SMGs', 'Rifles', 'AWP', 'Autosnipers']

warlock = DNDClass('Warlock', 'A Witch/Warlock serves a greater patron for a chance at greater power.', requiredClasses={cleric:7, sorcerer:7}, save=['Wisdom', 'Charisma'])
warlock.weapons = list(chain(knife, pistols, grenades))
warlock.weaponDesc = ['Pistols', 'Grenades', 'Taser']

bard = DNDClass('Bard', 'Bards sing songs of encouragement to help their allies and hinder their enemies.', requiredClasses ={cleric:7, rogue:7}, save=['Dexterity', 'Charisma'])
bard.weapons = list(chain(knife, pistols, heavypistols, shotguns, smg, {'ssg08'}, grenades))
bard.weaponDesc = ['Pistols', 'Heavy Pistols', 'Shotguns', 'SMGs', 'Scout', 'Grenades', 'Taser']

ranger = DNDClass('Ranger', 'Rangers master the wilderness, hunting foes of their choosing.', requiredClasses={rogue:7, fighter:7}, save=['Dexterity', 'Strength'])
ranger.weapons = list(chain(knife, pistols, heavypistols, shotguns, smg, {'ssg08'}, grenades))
ranger.weaponDesc = ['Pistols', 'Heavy Pistols', 'Shotguns', 'SMGs', 'Scout', 'Grenades', 'Taser']

druid = DNDClass('Druid')
barbarian = DNDClass('Barbarian')
        
class Race():
    
    races = []
    defaultRace = None
    
    def __init__(self, name, description=None, levelAdjustment=0, defaultRace=False, weapons=[]):
        
        self.name = name
        self.weapons = weapons
        self.description=description
        levelAdjustment = levelAdjustment
        if defaultRace:
            if not Race.defaultRace:
                Race.defaultRace = self
        Race.races.append(self)
                
human = Race('Human', 'Humans excel at learning and gain bonus XP', defaultRace = True)
elf = Race('Elf', 'Elves are graceful and trained in many weapons')
elf.weapons = list(chain({'m4a1', 'm4a1_silenced', 'ak47', 'ssg08'}))
elf.weaponDesc = ['M4', 'AK-47', 'Scout']
halfling = Race('Halfling', 'Halflings are short and nimble making them hard to see')
dwarf = Race('Dwarf', 'Dwarves have a stronger stomach from years of drinking and mining')
dragonborn = Race('Dragonborn', 'Humanoid dragons that can breath fire upon their enemies')
gnome = Race('Gnome', 'Gnomes are clever inventors and engineers')
halfelf = Race('Half-Elf', 'Half-Elves make charming scholars and diplomats')
halforc = Race('Half-Orc', "Half-Orcs aren't nearly as brutish as full-bloods, but nearly as strong")
tiefling = Race('Tiefling', 'Tieflings blood have been tainted with infernal ancestry')

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
        self.save = None
        if getSteamid(self.userid) in database:
            self.stats = database[getSteamid(self.userid)]
        else:
            messageServer("Welcome the new player, %s!"%self.name)
            self.setClass(DNDClass.defaultClass.name)
            self.setRace(Race.defaultRace.name)
            self.stats['Gold'] = 0
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
        
        self.stats[self.getClass()]['XP'] += xp
        message = "\x06You have earned %s XP"%xp
        if reason:
            message += " for %s!"%reason
        else:
            message += "!"            
        message += " %s/%sXP"%(self.getXP(), self.getLevel()*1000)
        messagePlayer(message, self.index)
        
        if self.getLevel() < 20:
            xpNeeded = self.getLevel() * 1000
            while self.getXP() >= xpNeeded:
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
            self.save = cls.save
        else:
            messagePlayer("You haven't unlocked that class yet", self.index)
        
        
    def getRace(self):
        return self.stats['Race']
        
    def setRace(self, race):
        
        if race in Race.races:
            self.stats['Race'] = race.name
            messagePlayer('You are now a %s'%race.name, self.index)
            return True
        
        for r in Race.races:
            if r.name == race:
                self.stats['Race'] = race
                messagePlayer('You are now a %s'%race, self.index)
                return True
                
        error("%s IS NOT A VALID RACE"%race.name)
            
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
        return (self.getLevel() - 1) / 4
        
    def getSaves(self):
    
        cls = self.getClass()        
        for c in DNDClass.classes:
            if cls == c.name:
                return c.save
                
    def heal(self, amount):
        if self.health != self.maxhealth:
            healed = self.health
            self.health = min(self.maxhealth, self.health + amount)
            healed = self.health - healed
            return healed
        return 0
        
    def resetBuffs(self):
        self.buff = False
        self.curse = False
        
        
players = PlayerDictionary(RPGPlayer)

def formatLine(line, menu):

    line = line.split(' ')
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
        player = players.from_userid(userid_from_index(index))
        if choice.value:
            if player.dead:
                if choice.value in Race.races:
                    player.setRace(choice.value)
                if choice.value in DNDClass.classes:
                    player.setClass(choice.value)
            else:
                messagePlayer("You have to be dead to change your race or class.", index)

    confirmationMenu = PagedMenu(title="Play a %s?"%obj.name)
    confirmationMenu.append(PagedOption("Yes", obj))
    confirmationMenu.append(PagedOption("No", None))
    
    formatLine(obj.description, confirmationMenu)
    if obj in DNDClass.classes:
        formatLine('Good Save(s): ' + str(obj.save).strip("[]").replace("'", ""), confirmationMenu)
    if obj.weapons:
        formatLine('Weapons: '+ str(obj.weaponDesc).strip("[]").replace("'", ""), confirmationMenu)
    confirmationMenu.select_callback = confirmationMenuSelect
    confirmationMenu.send(index)

def dndMenuSelect(menu, index, choice):    
    if choice.value:
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
dndMenu.append(PagedOption('Player Info', dndPlayerInfoMenu))
dndMenu.append(PagedOption('Commands', None))
dndMenu.append(PagedOption('Help', None))
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
    weapon = make_object(Entity, stack_data[1])    
    player = players.from_userid(Player(make_object(Entity, stack_data[0]).index).userid)
    weaponName = weapon.classname.replace('weapon_', '')
    if not player.canUseWeapon(weaponName):
        if hasattr(player, 'lastWeaponMessage'):
            if time.time() - player.lastWeaponMessage > 2:
                player.lastWeaponMessage = time.time()
                messagePlayer('%s\'s can not use a %s'%(player.getClass(),weaponName), player.index)
        else:
            player.lastWeaponMessage = time.time()
            messagePlayer('You can not use a %s'%weaponName, player.index)
        return False        
            
#@OnPlayerRunCommand
def on_player_run_command(player, user_cmd):
    player = database.from_userid(player.userid)    
    if player.hasPerk(hundredM.name):
        if user_cmd.buttons & PlayerButtons.SPEED:
            player.speed = 2.5 + player.getPerkLevel(hundredM.name)*hundredM.effect
            pass
        else:
            player.speed = 1
            
    if player.hasPerk(marathon.name):
        if user_cmd.buttons & PlayerButtons.FORWARD:
            player.speed = 1 + player.getPerkLevel(marathon.name)*marathon.effect
    
    if user_cmd.buttons & PlayerButtons.USE:
        pass

def load():
    global players
    info = plugin_manager.get_plugin_info('dnd5e')
    SayText2("%s - %s has been loaded"%(info.verbose_name,info.version)).send()
    print(("%s - %s has been loaded"%(info.verbose_name,info.version)))
    loadDatabase()
    players = PlayerDictionary(RPGPlayer)
        
    
def loadDatabase():
    global database
    if not os.path.exists(databaseLocation):
        newDatabase()
    else:
        with open(databaseLocation, 'r') as db:
            database = json.load(db)
            
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
    purgeTime = 60 * 60 * 24 * 0 # 15 days
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
        
        
@Event('round_end')
def endedRound(e):
    for player in PlayerIter():
        if e['winner'] == player.team_index:
            players.from_userid(player.userid).giveXP(roundWinXP, "wining the round!")    
    saveDatabase()
            
@Event('player_say')
def playerSay(e):
    global database
    if e['userid'] != 0:
        steamid = getSteamid(e['userid'])
        player = players.from_userid(e['userid'])
        if not player.is_bot():
        
            if e['text'].lower() == 'menu':
                dndMenu.send(player.index)
        
            if e['text'].lower() == 'playerinfo':
                showPlayerInfo(player.index)        
            
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
        
@Event('player_hurt')
def damagePlayer(e):
    # will detect special infected / how to separate?
    if e['attacker'] != 0 and e['userid'] != 0:
        attacker = players.from_userid(e['attacker'])

        victim = players.from_userid(e['userid'])
        weapon = attacker.get_active_weapon()
        damage = int(e['dmg_health'])
        
        if victim.team_index != attacker.team_index:
        
            # Check for true dodging :^)
            if damage > 0:
                        
                if attacker.getClass() == fighter.name:
                    
                    if attacker.getLevel() >= 3:
                    
                        # Great Weapon Master
                        if attacker.crit:                        
                            enemies = {}
                            for p in PlayerIter():
                                if p.team_index != attacker.team_index and not p.dead:
                                    distance = Vector.get_distance(victim.origin, p.origin)
                                    enemies[p] = distance
                            enemies = {k: v for k, v in sorted(enemies.items(), key=lambda item: item[1])}
                            enemies = list(enemies.keys())
                            cleaveTarget = enemies[0]
                            if cleaveTarget.index == victim.index:
                                if len(enemies) > 1:
                                    cleaveTarget = enemies[1]
                                else:
                                    return
                            hurt(attacker,players.from_userid(cleaveTarget.userid),int(damage/2))                        
                            
                    if attacker.getLevel() >= 7:
                        
                        if attacker.disarm and attacker.disarms:
                            if diceCheck(( 11 + attacker.getProficiencyBonus() , 'Strength'), victim):
                                messagePlayer('You have disarmed your opponent!', attacker.index)
                                messagePlayer('You have been disarmed!', victim.index)
                                weapon = victim.get_active_weapon()
                                name = weapon.classname
                                weapon.remove()
                                Delay(1.5, giveItem, (victim, name))
                            else:
                                messagePlayer('Your disarm has failed!', attacker.index)
                            attacker.disarms -= 1
                            attacker.disarm = False
                        
def giveItem(player, weaponName):
    player.give_named_item(weaponName)
    
@EntityPreHook(EntityCondition.is_player, 'on_take_damage')
def preDamagePlayer(stack_data):
    # if 'riot' in victim.get_model().path
    victim = make_object(Entity, stack_data[0])
    if not victim.is_player:
        return
    info = make_object(TakeDamageInfo, stack_data[1])    
    if not info.inflictor > 0:
        return
        
    attacker = None 
    try: 
        attacker = players.from_userid(Player(info.inflictor).userid)
    except:
        pass

    if attacker:
        victim = players.from_userid(Player(victim.index).userid)
        
        if victim.team_index != attacker.team_index:
        
            info.damage = formatDamage(attacker, victim, info.damage, info.weapon)
            
            
        
                
def hurt(attacker, victim, amount, spell=False):

    amount = formatDamage(attacker, victim, amount, 'point_hurt')

    if victim.health > amount:        
        victim.health -= amount
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
        entity.remove
        
        victim.target_name = targetName
        
def formatDamage(attacker, victim, damage, weapon=None):
    
    #Dodge shit here. Can still dodge spell damage
    if victim.getClass() == fighter.name and victim.getLevel() >= 10:
        if victim.armor > 0:
            if random.randint(1,20) == 20:
                messagePlayer('You parried an attack with your defensive techniques!', victim.index)
                messagePlayer('Your target parried your attack!', attacker.index)
                return 0
    
        
    # attacker shit here. 
    # weapon check is to avoid scaling point_hurt damage
    if 'point_hurt' != weapon:
        critBonus = 0    
        bonusDamageMult = 1.0
        
        if attacker.getClass() == fighter.name:
            bonusDamageMult += .1
            
            if attacker.getLevel() >= 3:
                critBonus += 1
            if attacker.getLevel() >= 5:
                bonusDamageMult += .05
            if attacker.getLevel() >= 11:
                bonusDamageMult += .05
            if attacker.getLevel() >= 15:
                critBonus += 1
         
        damage *= bonusDamageMult 
         
        if random.randint(1+critBonus,20) >= 20:
            damage *= 2
            damage = int(damage)
            messagePlayer('You dealt a critical hit for %s damage!'%damage, attacker.index)
            messagePlayer('You were dealt a critical hit for %s damage!'%damage, victim.index)
            attacker.crit = True
        else:
            attacker.crit = False
            
    #Cursed targets DO scale spell damage
    if hasattr(victim, 'curse'):
        if victim.curse:
            damage += dice(3,8)
    
    return damage
    
@Event('player_death')
def killedPlayer(e):
    if e['attacker'] != 0 and e['userid'] != 0:
        attacker = players.from_userid(e['attacker'])

        victim = players.from_userid(e['userid'])
        weapon = attacker.get_active_weapon()
        
        victim.resetBuffs()
        
        if victim.team_index != attacker.team_index:
        
            if e['headshot']:
                attacker.giveXP(headshotXP, 'a headshot!')
            else:
                attacker.giveXP(killXP, 'a kill!')
        
            if attacker.getClass() == fighter.name:
                if attacker.getLevel() == 20:
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
    '''
    if weapon.index in spawnedWeapons:
        weapon.ammo = weapon.clip * 2
        spawnedWeapons.remove(weapon.index)
    if player.hasPerk("Finger Guns"):
        player.delay(0, weapon_fire_post, (player,))
    '''
    
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
    
@Event('player_spawn')
def spawnPlayer(e):
    player = players.from_userid(e['userid'])
    player.maxhealth = 100    
        
    if player.getClass() == fighter.name:
        player.secondWind = 1
        messagePlayer('You gained 10% damage from Greater Weapon Fighting!', player.index)
        
        if player.getLevel() >= 3:
            messagePlayer('You have an extra 5% chance to score a critical hit!', player.index)
            
        if player.getLevel() >= 5:
            messagePlayer('You deal an extra 5% damage for having an Extra Attack!', player.index)
        
        if player.getLevel() >= 7:
            player.disarms = int((player.getLevel() - 2) / 5)   #+ 10000
            messagePlayer('You have %s Disarms left. !cast Disarm (Strength save negates)'%player.disarms, player.index)
            player.disarm = False
        
        if player.getLevel() >= 9:
            player.indomitable = 1
        if player.getLevel() >= 13:
            player.indomitable = 2            
        if player.getLevel() >= 9:
            messagePlayer('You are now Indomitable (reroll %s failed saves)'%player.indomitable, player.index)
            
        if player.getLevel() >= 10:
            messagePlayer('You have a 5% chance to parry attacks!', player.index)
            
        if player.getLevel() >= 11:
            messagePlayer('You deal an extra 5% damage for having another Extra Attack!', player.index)
            
        if player.getLevel() >= 15:
            messagePlayer('You have an extra 5% chance to score a critical hit! A 15% Chance!!!', player.index)
            
        if player.getLevel() >= 20:
            messagePlayer('You are a Survivor! Heal 10HP every kill!', player.index)
            
    if player.getClass() == cleric.name:
        player.mana = player.getLevel() * 10
        messagePlayer('You have %s mana to cast spells with'%player.mana, player.index)
        if not hasattr(player, 'alignment'):
            player.alignment = 'good'
        if player.alignment == 'good':
            messagePlayer('You are a Good Cleric and do 20% more Curing', player.index)
        else:
            messagePlayer('You are an Evil Cleric and cause 20% more Wounds', player.index)
        messagePlayer('You can change your alignment with !cast {Evil/Good}', player.index)
        messagePlayer('!cast Inflict {amount} / !cast Cure {amount}', player.index)
        messagePlayer('Inflict to deal damage, Cure to heal. Spend up to %s mana (1HP/mana)'%(min(player.mana, player.getLevel()*2+10)), player.index)
        
        if player.getLevel() >= 3:
            messagePlayer('!cast Sacred Flame - 15 mana - %sd8 damage + burn (Dexterity save for half damage)'%(3+player.getLevel()/5), player.index)
            messagePlayer('!cast Bless - 10 mana - Increase chance for nearby allies to save', player.index)
            
        if player.getLevel() >= 5:
            messagePlayer('!cast Spiritual Weapon {weapon} - 30 mana - Give yourself a weapon (give command)', player.index) 
            messagePlayer('!cast Curse - 50 mana - Target takes additional 3d8 damage from all sources (Wisdom save negates)', player.index)
            
        if player.getLevel() >= 7:
            player.channels = (player.getLevel() - 2) / 5
            messagePlayer('!cast Channel Divinity - Unleash a burst of Healing/Good or Damage/Evil around you (5d8, %s uses)'%player.channels, player.index)

abilities = {
    'second wind',
    'cure',
    'inflict',
    'sacred flame',
    'bless',
    'spiritual weapon',
    'curse',
    'channel divinity'
}

toggles = {
    'evil',
    'good',
    'disarm'
}

@ClientCommand('!cast')
def cast(command, index):
    
    a = command.arg_string if len(command) > 1 else messagePlayer("You didn't specify an ability to use", index)
    ability = a
    amount = None
    
    if ability.lower().startswith('cure') or ability.lower().startswith('inflict'):
        ability = ability.split(' ')[0]
        try:
            amount = int(a.split(' ')[1])
        except:
            messagePlayer('You specify how much to heal/damage: !cast Cure 10', player.index)
            return
    
    if ability.lower().startswith('spiritual weapon'):
        ability = 'spiritual weapon'
        try:
            amount = a.split(' ')[2]
        except:
            messagePlayer('You need to specify which weapon: !cast Sacred Flame {weapon}', player.index)
            return

    if ability.lower() not in abilities:
        if ability.lower() not in toggles:
            messagePlayer("'%s' is not an ability"%ability, index)
            return
    player = players.from_userid(Player(index).userid)
        
    if ability.lower() in abilities:
        if not player.dead:      
            if time.time() - player.spellCooldown > 1.5:
                
                if player.getClass() == fighter.name:
                    if ability.lower() == 'second wind':
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
                    
                    if ability.lower() in ['inflict', 'cure']:
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
                            if ability.lower() == 'inflict':
                                if target.team != player.team and not target.dead:
                                    damage = amount
                                    if player.alignment == 'evil':
                                        damage = int(amount * 1.2)
                                    messagePlayer('You Inflicted Wounds for %s damage!'%damage, player.index)
                                    messagePlayer('You were Inflicted with Wounds!', target.index)
                                    hurt(player, target, amount, spell=True)
                                    
                                    player.spellCooldown = time.time()
                                    player.mana -= amount
                                    
                            if ability.lower() == 'cure':
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
                                
                        
                            
                    if ability.lower() == 'sacred flame':
                        if not player.getLevel() >= 3:
                            return
                        if not player.mana >= 15:
                            messagePlayer('You do not have enough mana for this spell %s/%s'%(player.mana, 15), player.index)
                            return
                        target = player.get_view_player()
                        if not target:
                            return
                        target = players.from_userid(target.userid)
                        if target.team != player.team and not target.dead:
                            player.mana -= 15
                            player.spellCooldown = time.time()
                            damage = dice((3+player.getLevel()/5),8)
                            if diceCheck((11 + player.getProficiencyBonus(), 'Dexterity'), target):
                                messagePlayer('You smote %s for %s damage!'%(target.name, int(damage/2)), player.index)
                                messagePlayer('You were smitten!', target.index)
                                hurt(player, target, int(damage/2))                                
                            else:
                                messagePlayer('You burned %s for %s damage!'%(target.name, int(damage)), player.index)
                                messagePlayer('You were smitten with fire!', target.index)
                                hurt(player, target, int(damage))
                                target.ignite_lifetime(1.7+.2*player.getLevel())
                            
                    if ability.lower() == 'bless':
                        if not player.getLevel() >= 3:
                            return
                        if not player.mana >= 10:
                            messagePlayer('You do not have enough mana for this spell %s/%s'%(player.mana, 15), player.index)
                            return
                        player.mana -= 10
                        player.spellCooldown = time.time()
                        for target in PlayerIter():
                            if target.team == player.team and not target.dead:
                                if Vector.get_distance(target.origin, player.origin) < 500:
                                    if not hasattr(target.bless):
                                        target.bless = True
                                        messagePlayer('You have been Blessed by a Cleric. Increases your chance to make saves!', target.index)
                                    else:
                                        if not target.bless:
                                            target.bless = True
                                            messagePlayer('You have been Blessed by a Cleric. Increases your chance to make saves!', target.index)
                                    
                            
                    if ability.lower() == 'spiritual weapon':
                        if not player.getLevel() >= 5:
                            return
                        if not player.mana >= 30:
                            messagePlayer('You do not have enough mana for this spell %s/%s'%(player.mana, 30), player.index)
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
                            
                    if ability.lower() == 'curse':
                        if not player.getLevel() >= 5:
                            return
                        if not player.mana >= 50:
                            messagePlayer('You do not have enough mana for this spell %s/%s'%(player.mana, 50), player.index)
                            return
                        target = player.get_view_player()
                        if not target:
                            return
                        target = players.from_userid(target.userid)
                        if target.team != player.team and not target.dead:
                            player.mana -= 50
                            player.spellCooldown = time.time()       
                            if not diceCheck((11 + player.getProficiencyBonus(), 'Wisdom'), target):
                                target.curse = True
                                messagePlayer('You have Cursed %s'%target.name, player.index)
                                messagePlayer('You have been Cursed!', target.index)
                            else:
                                messagePlayer('Your target resists your curse!', player.index)
                                
                    if ability.lower() == 'channel divinity':
                        if not player.getLevel() >= 7:
                            return
                        if not player.channels > 0:
                            messagePlayer('You have no more uses of Channel Divinity', player.index)                            
                            return
                        
                        player.channels -= 1
                        player.spellCooldown = time.time()
                        if player.alignment.lower() == 'good':
                            for p in PlayerIter():
                                if not p.dead and p.team == player.team and Vector.get_distance(player.origin, p.origin) < 700:
                                    target = players.from_userid(p.userid)
                                    hp = target.heal(dice(5,8))
                                    if hp:
                                        messagePlayer('Your Channel Divinity healed %s for %s HP!'%(target.name, hp), player.index)
                                        messagePlayer('You were healed by %s\'s Divine Power'%player.name, target.index)
                                        
                        if player.alignment.lower() == 'evil':
                            for p in PlayerIter():
                                if not p.dead and p.team == player.team and Vector.get_distance(player.origin, p.origin) < 700:
                                    target = players.from_userid(p.userid)
                                    damage = dice(5,8)
                                    messagePlayer('You were assaulted by %s\'s Divine Power'%player.name, target.index)
                                    messagePlayer('Your Channel Divinity caused %s wounds to %s!'%(damage, target.name), player.index)
                                    hurt(player, target, damage)
                        
            else:
                messagePlayer('Your spells and abilities are on cooldown!', index)
    #is a toggle
    else:
        if time.time() - player.toggleDelay > 0.1:
            
            if player.getClass() == fighter.name:
                if not player.dead:
                    if ability.lower() == 'disarm':
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
                if ability.lower() in ['evil', 'good']:
                    if player.dead:
                        player.alignment = ability.lower()
                        messagePlayer('You are now a %s Cleric'%ability, player.index)
                        player.toggleDelay = time.time()
                    else:
                        messagePlayer('You must be dead to change your alignment', player.index)
                        
    
    return CommandReturn.BLOCK
    
    
