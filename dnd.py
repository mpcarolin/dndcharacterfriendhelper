# coding: utf8
import os
import json

class Character(object):
    def __init__(self, name, spells, race, hp, speed, gold=0, silver=0, copper=0, weapons=[]):
        self.name = name
        self.spells = spells
        self.gold = gold
        self.silver = silver
        self.copper = copper
        self.race = race
        self.hp = hp
        self.total_hp = hp
        self.speed = speed
        self.weapons = weapons
        self.current_weapon = None

    def __json__(self):
        return {
            "name": self.name,
            "spells": json.dumps(self.spells, default=lambda spell: spell.__json__()),
            "gold": self.gold,
            "silver": self.silver,
            "copper": self.copper,
            "race": self.race,
            "hp": self.hp,
            "total_hp": self.total_hp,
            "speed": self.speed,
            "weapon": json.dumps(self.weapons, default=lambda weapon: weapon.__json__()),
        }

    @staticmethod
    def fromJson(json_str):
        json_map = json.loads(json_str)
        return Character(
           json_map["name"],
           Spell.fromJson(json_map["spells"]),
           json_map["race"],
           int(json_map["hp"]),
           int(json_map["speed"]),
           int(json_map["gold"]),
           int(json_map["silver"]),
           int(json_map["copper"]),
           Weapon.fromJson(json_map["weapons"])
        )

    def saveCharacter(self):
        os.system('cls' if (os.name == 'nt') else 'clear')
        print "------------------------------------------------"
        f_path = "./characters/" + self.name + ".json"
        f = open(f_path, "w")
        f.write(json.dumps(self.__json__()))
        f.close()

        print "Character Saved!"
        print "------------------------------------------------"
        raw_input("Press enter to continue...")
        os.system('cls' if (os.name == 'nt') else 'clear')


    def equipWeapon(self): pass

    def addNewWeapon(self):
        print "------------------------------------------------"
        print "ADD A NEW WEAPON"
        name = raw_input("Enter the weapon name: ")
        w_type = raw_input("Enter the weapon type: ")
        die = raw_input("Enter the attack's dice type (4,6,8...): ")
        num_dice = raw_input("Enter the number of dice rolled on an attack: ")
        weapon = Weapon(name, w_type, die, num_dice)
        self.weapons.append(weapon)
        print "------------------------------------------------"

        choice = raw_input("Equip? [Y\N] ").lower()
        if (choice == "y"):
            self.current_weapon = weapon
            print weapon.name + " equipped!"

        raw_input("Press enter to continue...")
        os.system('cls' if (os.name == 'nt') else 'clear')


    def showInfoPage(self):
        spells = self.spells
        commands = ["set", "drop", "add", "new", "save"]

        # sort spells by level
        sorted(spells, key=lambda x: x.tier)

        choice = None
        while (choice != 'q' and choice != 'quit'):
            os.system('cls' if (os.name == 'nt') else 'clear')
            if (choice is not None):
                if (choice.isdigit()):
                    print "------------------------------------------------"
                    print spells[int(choice)-1]
                    print "------------------------------------------------"
                    raw_input("Press enter to continue...")
                    os.system('cls' if os.name == 'nt' else 'clear')
                else:
                    params = choice.split()
                    if (len(params) == 0 or params[0].lower() not in commands):
                        print "Unrecognized command. Try the form [command] [attribute] [amount]"
                    else:
                        command = params[0].lower()
                        attribute = params[1].lower()
                        if (len(params) == 3):
                            amount = int(params[2])
                        if (command == "set"):
                            if (attribute == "gold"):
                                self.gold = amount
                            elif (attribute == "silver"):
                                self.silver = amount
                            elif (attribute == "copper"):
                                self.copper = amount
                            elif (attribute == "hp"):
                                self.hp = amount
                                self.total_hp = amount
                        elif (command == "drop"):
                            if (attribute == "gold"):
                                self.gold -= amount
                            elif (attribute == "silver"):
                                self.silver -= amount
                            elif (attribute == "copper"):
                                self.copper -= amount
                            elif (attribute == "hp"):
                                self.hp -= amount
                        elif (command == "add"):
                            if (attribute == "gold"):
                                self.gold += amount
                            elif (attribute == "silver"):
                                self.silver += amount
                            elif (attribute == "copper"):
                                self.copper += amount
                            elif (attribute == "hp"):
                                self.hp += amount
                        elif (command == "new"):
                            if (attribute == "weapon"):
                                self.addNewWeapon()
                        elif (command == "save"):
                            if (attribute == "character"):
                                self.saveCharacter()
                         
            print "------------------------------------------------"
            print "\t\t CHARACTER"
            print self
            print "------------------------------------------------"
            print "\t\tSPELLS"
            lastTier = -1
            for i in xrange(len(spells)):
                spell = spells[i]
                if (spell.tier > lastTier):
                    lastTier = spell.tier
                    if (spell.tier == 0):
                        print "CANTRIPS"
                    else:
                        print "LEVEL " + str(spell.tier)
                print ("\t" + str(str(i+1) + ") " + spell.title))
            print "------------------------------------------------"
            print "\t\tWEAPONS"
            for weapon in self.weapons:
                if (weapon is not self.weapons[0]):
                    print "\t------------------------"
                print str(weapon)
            print "------------------------------------------------"

            choice = raw_input("Select a spell, type a command, or type q to quit: ")

    def __str__(self):
        s = "Name: " + self.name
        s += "\nRace: " + self.race
        s += "\n\nHP: " + str(self.hp) + "/" + str(self.total_hp)
        s += "\nSpeed: " + str(self.speed)
        s += "\n" + "Gold: " + str(self.gold) + ", Silver: " 
        s += str(self.silver) + ", Copper: " + str(self.copper)
        return s

class Weapon(object):
    def __init__(self, name, w_type, die, num_dice):
        self.name = name            # name of weapon
        self.w_type = w_type        # weapon type (e.g. melee)
        self.die = die
        self.num_dice = num_dice

    # Returns a tuple with the attack roll result first and the damage second
    def attack():
        attack_roll = (int)(random.random() * 20)
        damage = 0
        for roll in xrange(num_dice):
            damage += random.random() * self.die
        return (attack_roll, damage)

    def __json__(self):
        return {
            "name": self.name,
            "type": self.w_type,
            "die": self.die,
            "num_dice": self.num_dice
        }

    def __str__(self):
        s = "Name: " + self.name + "\n"
        s += "Type: " + self.w_type + "\n"
        s += "Damage: " + self.num_dice + " D" + self.die
        return s

class Spell(object):
    def __init__(self, title, tier, rang, duration, description, action_cost):
        self.title = title
        self.tier = tier
        self.description = description
        self.rang = rang
        self.duration = duration
        self.action_cost = action_cost

    def __str__(self):
        s = "\t Title: " + self.title + "\n"
        s += "\t Range: " + self.rang + "\n"
        s += "\t Duration: " + self.duration + "\n"
        s += "\t Cost: " + self.action_cost + "\n\n"
        s += self.description + "\n"
        return s

    def __json__(self):
        return {
            "title":self.title,
            "range": self.rang,
            "duration": self.duration,
            "tier": self.tier,
            "action_cost": self.action_cost,
            "description": self.description
        }
    

gold = 123
silver = 23
copper = 5
spells = []

# spells 
spells.append(Spell(
        title="Friends", 
        tier=0,
        rang="Self",
        duration="Concentrtion, 1 minute",
        description="For the duration, you have advantage on all Charisma checks directed at one creature of your choice that isn’t hostile toward you. When the spell ends, the creature realizes that you used magic to influence its mood and becomes hostile toward you. A creature prone to violence might attack you. Another creature might seek retribution in other ways (at the DM’s discretion), depending on the nature of your interaction with it.",
        action_cost="1"
))
spells.append(Spell(
        title="Vicious Mockery", 
        tier=0,
        rang="60 Feet",
        duration="Instantaneous",
        description="You unleash a string of insults laced with subtle enchantments at a creature you can see within range. If the target can hear you (thought it need not understand you), it must succeed on a Wisdom saving throw or take 1d4 psychic damage and have disadvantage on the next attack roll it makes before the end of its next turn. At higher level this spell’s damage increases by 1d4 when you reach 5th level (2d4), 11th level (3d4), and 17th level (4d4).",
        action_cost="1"
))

spells.append(Spell(
        title="Minor Illusion", 
        tier=0,
        rang="30 feet",
        duration="1 minute",
        description="You create a sound or an image of an object within range that lasts for the duration. The illusion also ends if you dismiss it as an action or cast this spell again. If you create a sound, its volume can range from a whisper to a scream. It can be your voice, someone else’s voice, a lion’s roar, a beating of drums, or any other sound you choose. The sound continues unabated throughout the duration, or you can make discrete sounds at different times before the spell ends. If you create an image of an object such as a chair, muddy footprints, or a small chest must be no larger than a 5-foot cube. The image can’t create sound, light, smell, or any other sensory effect. Physical interaction with the image reveals it to be an illusion, because things can pass through it. If a creature uses its action to examine the sound or image, the creature can determine that it is an illusion with a successful Intelligence (Investigation) check against your spell save DC. If a creature discerns the illusion for what it is, the illusion becomes faint to the creature.",
        action_cost="1"
))

spells.append(Spell(
        title="Bane", 
        tier=1,
        rang="30 feet",
        duration="Concentration, 1 minute",
        description="Up to three creatures of your choice that you can see within range must make Charisma saving throws. Whenever a target that fails this saving throw makes an attack roll or a saving throw before the spell ends, the target must roll a d4 and subtract the number rolled from the attack roll or saving throw. At higher level. When you cast this spell using a spell slot of 2nd level or higher, you can target one addtional creature for each slot level above 1st.",
        action_cost="1"
))

spells.append(Spell(
        title="Bless", 
        tier=1,
        rang="30 feet",
        duration="Concentration, 1 minute",
        description="A sprinkling of holly water. You bleed 3 creatures of choice within range. Whenever a target makes an attack roll or a saving throw before the spell ends, the target can roll a d4 and add the number rolled to the attack roll or saving throw. HIGHER LEVEL: when you cast this spell using a spell slot of 2nd level or higher, you can target one additional creature for each slot above 1.",
        action_cost="1"
))

spells.append(Spell(
        title="Cure Wounds", 
        tier=1,
        rang="Touch",
        duration="Instantaneous",
        description="A creature you touch regains a number of hit points equal to 1d8 + your spellcasting ability modifier. This spell has no effect on undead or constructs. At higher level: increases by 1d8 for each slot level above 1.",
        action_cost="1"
))
    
spells.append(Spell(
        title="Entangle", 
        tier=1,
        rang="90 feet",
        duration="Concentration, 1 minute",
        description="Grasping weeds and vines sprout from the ground in a 20-foot square starting from a point within range. For the duration, these plants turn the ground in the area into difficult terrain.A creature in the area when you cast the spell must succeed on a Strength saving throw or be restrained by the entangling plants until the spell ends. A creature restrained by the plants can use its action to make a Strength check against your spell save DC. On a success, it frees itself. Conjured plants wilt away at spell end.",
        action_cost="1"
))

spells.append(Spell(
        title="Healing Word", 
        tier=1,
        rang="60 feet",
        duration="Instantaneous",
        description="A creature of your choice that you can see within range regains hit points equal to 1d4 + your spellcasting ability modifier. This spell has no effect on undead or constructs. HIGHER LEV: healing increases by 1d4 for each slot level above 1.",
        action_cost="1 Bonus Action"
))

spells.append(Spell(
        title="Blindness/Deafness", 
        tier=2,
        rang="30 feet",
        duration="Instantaneous",
        description="You can blind or deafen a foe. Choose one creature that you can see within range to make a Constitution saving throw. If it fails, the target is either blinded or deafened (your choice) for the duration. At the end of each of its turns, the target can make a Constitution saving throw. On a success, the spell ends. HIGHER LEV: when in 3rd lev slot, target +1 create for each slot level above 2.", 
        action_cost="1 Bonus Action"
))

spells.append(Spell(
        title="Invisibility", 
        tier=2,
        rang="Touch",
        duration="Concentration, 1 HOUR",
        description="One touch imparts a magic bonus. One of the following: - Bear’s Endurance. The target has advantage on Constitution checks. It also gains 2d6 temporary hit points, which are lost when the spell ends. - Bull’s Strength. The target has advantage on Strength checks, and his or her carrying capacity doubles. - Cat’s Grace. The target has advantage on Dexterity checks. It also doesn’t take damage from falling 20 feet or less if it isn’t incapacitated. - Eagle’s Splendor. The target has advantage on Charisma checks. - Fox’s Cunning. The target thas advantage on Intelligence checks.- Owl’s Wisdom. The target has advantage on Wisdom checks.",
        action_cost="1 Action"
))

spells.append(Spell(
        title="Hypnotic Pattern", 
        tier=3,
        rang="120 Feet",
        duration="Concentration, 1 Minute",
        description="You create a twisting pattern of colors that weaves through the air inside a 30-foot cube within range. The pattern appears for a moment and vanishes. Each creature in the area who sees the pattern must make a Wisdom saving throw. On a failed save, the creature becomes charmed for the duration. While charmed by this spell, the creature is incapacitated and has a speed of 0. The spell ends for an affected creature if it takes any damage or if someone else uses an action to shake the creature out of its stupor.",
        action_cost="1 Action"
))

def main():

    os.system('cls' if os.name == 'nt' else 'clear')
    choice = ""
    bob = Character(
            name="Bob", 
            spells=spells, 
            race="Hill Dwarf",
            hp=52,
            speed=20,
            gold=gold, 
            silver=silver, 
            copper=copper
    )
    bob.showInfoPage()

if __name__ == '__main__':
    main()



