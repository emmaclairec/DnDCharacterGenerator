#!/usr/bin/env python3

import random
import markovify
import warnings
import math
import uuid
import traceback
import os
import io
from re import template
import pdfrw
from reportlab.pdfgen import canvas

warnings.filterwarnings('ignore')
wrkdir = os.getcwd()
pdf_filename = "Character Sheet Official.pdf"
backstories = "backstories.txt"


def roll_dice(d, num_dice, list=False):
    if list:
        all_rolls = []
        while (num_dice > 0):
            all_rolls.append(random.randint(1, d))
            num_dice -= 1
        return all_rolls
    else:
        total = 0
        while (num_dice > 0):
            total += random.randint(1, d)
            num_dice -= 1
        return total


class Abilities:
    class STR:
        name = "STR"
        score = 0
        mod = 0
        checkbox = "Check Box 11"

    class DEX:
        name = "DEX"
        score = 0
        mod = 0
        checkbox = "Check Box 18"

    class CON:
        name = "CON"
        score = 0
        mod = 0
        checkbox = "Check Box 19"

    class INT:
        name = "INT"
        score = 0
        mod = 0
        checkbox = "Check Box 20"

    class WIS:
        name = "WIS"
        score = 0
        mod = 0
        checkbox = "Check Box 21"

    class CHA:
        name = "CHA"
        score = 0
        mod = 0
        checkbox = "Check Box 22"

    list = [STR, DEX, CON, INT, WIS, CHA]


class Class:
    def __init__(self):
        pass

    class Barbarian():
        name = "Barbarian"
        prim_abil = [Abilities.STR]
        sav_throw = [Abilities.STR, Abilities.CON]
        align_tend = ["C", "N"]
        gold = roll_dice(4, 2) * -10

    class Bard():
        name = "Bard"
        prim_abil = [Abilities.CHA]
        sav_throw = [Abilities.DEX, Abilities.CHA]
        align_tend = ["C", "N"]
        gold = roll_dice(4, 5) * -10

    class Cleric():
        name = "Cleric"
        prim_abil = [Abilities.WIS]
        sav_throw = [Abilities.WIS, Abilities.CHA]
        align_tend = ["", ""]
        gold = roll_dice(4, 5) * -10

    class Druid():
        name = "Druid"
        prim_abil = [Abilities.WIS]
        sav_throw = [Abilities.INT, Abilities.WIS]
        align_tend = ["", ""]
        gold = roll_dice(4, 2) * -10

    class Fighter():
        name = "Fighter"
        prim_abil = [[Abilities.STR, Abilities.DEX][random.randint(0, 1)]]
        sav_throw = [Abilities.STR, Abilities.CON]
        align_tend = ["", ""]
        gold = roll_dice(4, 5) * -10

    class Monk():
        name = "Monk"
        prim_abil = [Abilities.DEX, Abilities.WIS]
        sav_throw = [Abilities.STR, Abilities.CON]
        align_tend = ["L", "N"]
        gold = roll_dice(4, 5) * -10

    class Paladin():
        name = "Paladin"
        prim_abil = [Abilities.STR, Abilities.CHA]
        sav_throw = [Abilities.STR, Abilities.CHA]
        align_tend = ["", ""]
        gold = roll_dice(4, 5) * -10

    class Ranger():
        name = "Ranger"
        prim_abil = [Abilities.DEX, Abilities.WIS]
        sav_throw = [Abilities.DEX, Abilities.WIS]
        align_tend = ["", ""]
        gold = roll_dice(4, 5) * -10

    class Rogue():
        name = "Rogue"
        prim_abil = [Abilities.DEX]
        sav_throw = [Abilities.DEX, Abilities.INT]
        align_tend = ["C", "N"]
        gold = roll_dice(4, 4) * -10

    class Sorcerer():
        name = "Sorcerer"
        prim_abil = [Abilities.CHA]
        sav_throw = [Abilities.CHA, Abilities.CON]
        align_tend = ["", ""]
        gold = roll_dice(4, 3) * -10

    class Warlock():
        name = "Warlock"
        prim_abil = [Abilities.CHA]
        sav_throw = [Abilities.WIS, Abilities.CHA]
        align_tend = ["", ""]
        gold = roll_dice(4, 4) * -10

    class Wizard():
        name = "Wizard"
        prim_abil = [Abilities.INT]
        sav_throw = [Abilities.INT, Abilities.WIS]
        align_tend = ["L", "N"]
        gold = roll_dice(4, 4) * -10

    list = [Barbarian, Bard, Cleric, Druid, Fighter, Monk, Paladin, Ranger, Rogue, Sorcerer, Warlock, Wizard]


class Race:
    class Dragonborn:
        name = "Dragonborn"
        base_height = (5 * 12) + 6
        height_mod_ran = [2, 16]
        base_weight = 175
        weight_mod_ran = [2, 8]
        max_age = 80
        ability_score = {Abilities.STR: 2, Abilities.CHA: 1}
        lang = ["Common"]
        align_tend = ["!N", "!N"]

    class Dwarf:
        class Hill:
            name = "Dwarf, Hill"
            base_height = (3 * 12) + 6
            height_mod_ran = [2, 8]
            base_weight = 115
            weight_mod_ran = [2, 12]
            max_age = 400
            ability_score = {Abilities.CON: 2, Abilities.WIS: 1}
            lang = ["Common", "Dwarvish"]
            align_tend = ["L", "G"]

        class Mountain:
            name = "Dwarf, Mountain"
            base_height = (3 * 12) + 6  # Check me!
            height_mod_ran = [2, 8]
            base_weight = 130
            weight_mod_ran = [2, 12]
            max_age = 400
            ability_score = {Abilities.CON: 2, Abilities.STR: 2}
            lang = ["Common", "Dwarvish"]
            align_tend = ["L", "G"]

        subcat = [Hill, Mountain]

    class Elf:
        class High:
            name = "Elf, High"
            base_height = (4 * 12) + 6
            height_mod_ran = [2, 20]
            base_weight = 90
            weight_mod_ran = [1, 4]
            max_age = 750
            ability_score = {Abilities.DEX: 2, Abilities.INT: 1}
            lang = ["Common"]
            align_tend = ["C", "G"]

        class Wood:
            name = "Elf, Wood"
            base_height = (4 * 12) + 6
            height_mod_ran = [2, 20]
            base_weight = 100
            weight_mod_ran = [1, 4]
            max_age = 750
            ability_score = {Abilities.DEX: 2, Abilities.WIS: 1}
            lang = ["Common"]
            align_tend = ["C", "G"]

        class Drow:
            name = "Elf, Drow"
            base_height = (4 * 12) + 5
            height_mod_ran = [2, 12]
            base_weight = 75
            weight_mod_ran = [1, 6]
            max_age = 750
            ability_score = {Abilities.DEX: 2, Abilities.CHA: 1}
            lang = ["Common"]
            align_tend = ["C", "E"]

        subcat = [High, Wood, Drow]

    class Gnome:
        class Rock:
            name = "Gnome, Rock"
            base_height = (2 * 12) + 11
            height_mod_ran = [2, 8]
            base_weight = 35
            weight_mod_ran = [1, 1]
            max_age = 500
            ability_score = {Abilities.INT: 2, Abilities.CON: 1}
            lang = ["Common"]
            align_tend = ["", "G"]

        class Forest:
            name = "Gnome, Forest"
            base_height = (2 * 12) + 11
            height_mod_ran = [2, 8]
            base_weight = 35
            weight_mod_ran = [1, 1]
            max_age = 500
            ability_score = {Abilities.INT: 2, Abilities.DEX: 1}
            lang = ["Common"]
            align_tend = ["", "G"]

        subcat = [Forest, Rock]

    class HalfElf:
        name = "Half-elf"
        base_height = (4 * 12) + 9
        height_mod_ran = [2, 16]
        base_weight = 110
        weight_mod_ran = [2, 8]
        max_age = 180
        ability_score = {Abilities.CHA: 2}
        lang = ["Common"]
        align_tend = ["C", ""]

    class HalfOrc:
        name = "Half-orc"
        base_height = (4 * 12) + 10
        height_mod_ran = [2, 20]
        base_weight = 140
        weight_mod_ran = [2, 8]
        max_age = 70
        ability_score = {Abilities.STR: 2, Abilities.CON: 1}
        lang = ["Common"]
        align_tend = ["C", "E"]

    class Halfling:
        class Lightfoot:
            name = "Halfling, Lightfoot"
            base_height = (2 * 12) + 7
            height_mod_ran = [2, 8]
            base_weight = 35
            weight_mod_ran = [1, 1]
            max_age = 150
            ability_score = {Abilities.DEX: 2, Abilities.CHA: 1}
            lang = ["Common"]
            align_tend = ["L", "G"]

        class Stout:
            name = "Halfling, Stout"
            base_height = (2 * 12) + 6
            height_mod_ran = [2, 8]
            base_weight = 36
            weight_mod_ran = [1, 1]
            max_age = 150
            ability_score = {Abilities.DEX: 2, Abilities.CON: 1}
            lang = ["Common"]
            align_tend = ["L", "G"]

        subcat = [Lightfoot, Stout]

    class Human:
        name = "Human"
        base_height = (4 * 12) + 8
        height_mod_ran = [2, 20]
        base_weight = 110
        weight_mod_ran = [2, 8]
        max_age = 100
        ability_score = {Abilities.STR: 1, Abilities.DEX: 1, Abilities.INT: 1, Abilities.WIS: 1,
                         Abilities.CON: 1, Abilities.CHA: 1}
        lang = ["Common"]
        align_tend = ["", ""]

    class Tiefling:
        name = "Tiefling"
        base_height = (4 * 12) + 9
        height_mod_ran = [2, 16]
        base_weight = 110
        weight_mod_ran = [2, 8]
        max_age = 100
        ability_score = {Abilities.INT: 1, Abilities.CHA: 2}
        lang = ["Common"]
        align_tend = ["C", "E"]

    list = [Dragonborn, Dwarf, Elf, Gnome, HalfElf, HalfOrc, Halfling, Human, Tiefling]


class Skills:
    class Acrobatics:
        name = "Acrobatics"
        score = Abilities.DEX
        checkbox = "Check Box 23"

    class AnimalHandling:
        name = "Animal Handling"
        score = Abilities.WIS
        checkbox = "Check Box 24"

    class Arcana:
        name = "Arcana"
        score = Abilities.INT
        checkbox = "Check Box 25"

    class Athletics:
        name = "Athletics"
        score = Abilities.STR
        checkbox = "Check Box 26"

    class Deception:
        name = "Deception"
        score = Abilities.CHA
        checkbox = "Check Box 27"

    class History:
        name = "History"
        score = Abilities.INT
        checkbox = "Check Box 28"

    class Insight:
        name = "Insight"
        score = Abilities.WIS
        checkbox = "Check Box 29"

    class Intimidation:
        name = "Intimidation"
        score = Abilities.CHA
        checkbox = "Check Box 30"

    class Investigation:
        name = "Investigation"
        score = Abilities.INT
        checkbox = "Check Box 31"

    class Medicine:
        name = "Medicine"
        score = Abilities.WIS
        checkbox = "Check Box 32"

    class Nature:
        name = "Nature"
        score = Abilities.INT
        checkbox = "Check Box 33"

    class Perception:
        name = "Perception"
        score = Abilities.WIS
        checkbox = "Check Box 34"

    class Performance:
        name = "Performance"
        score = Abilities.CHA
        checkbox = "Check Box 35"

    class Persuasion:
        name = "Persuasion"
        score = Abilities.CHA
        checkbox = "Check Box 36"

    class Religion:
        name = "Religion"
        score = Abilities.INT
        checkbox = "Check Box 37"

    class SleightofHand:
        name = "Sleight of Hand"
        score = Abilities.DEX
        checkbox = "Check Box 38"

    class Stealth:
        name = "Stealth"
        score = Abilities.DEX
        checkbox = "Check Box 39"

    class Survival:
        name = "Survival"
        score = Abilities.DEX
        checkbox = "Check Box 40"

    list = [Acrobatics, Arcana, Athletics, AnimalHandling, Deception, History, Insight, Intimidation, Medicine,
            Investigation, Nature, Perception, Performance, Persuasion, Religion, SleightofHand, Stealth, Survival]




class Backgrounds:
    class Acolyte:
        name = "Acolyte"
        skill_prof = [Skills.Insight, Skills.Religion]

    class Charlatan:
        name = "Charlatan"
        skill_prof = [Skills.Deception, Skills.SleightofHand]

    class Criminal:
        name = "Criminal"
        skill_prof = [Skills.Deception, Skills.Stealth]

    class Entertainer:
        name = "Entertainer"
        skill_prof = [Skills.Acrobatics, Skills.Performance]

    class FolkHero:
        name = "Folk Hero"
        skill_prof = [Skills.AnimalHandling, Skills.Survival]

    class GuildArtisan:
        name = "Guild Artisan"
        skill_prof = [Skills.Insight, Skills.Persuasion]

    class Hermit:
        name = "Hermit"
        skill_prof = [Skills.Medicine, Skills.Religion]

    class Noble:
        name = "Noble"
        skill_prof = [Skills.History, Skills.Persuasion]

    class Outlander:
        name = "Outlander"
        skill_prof = [Skills.Athletics, Skills.Survival]

    class Sage:
        name = "Sage"
        skill_prof = [Skills.Arcana, Skills.History]

    class Sailor:
        name = "Sailor"
        skill_prof = [Skills.Athletics, Skills.Perception]

    class Soldier:
        name = "Soldier"
        skill_prof = [Skills.Athletics, Skills.Intimidation]

    class Urchin:
        name = "Urchin"
        skill_prof = [Skills.SleightofHand, Skills.Stealth]

    bg_list = [Acolyte, Charlatan, Criminal, Entertainer, FolkHero, GuildArtisan, Hermit, Noble, Outlander, Sage,
               Sailor, Soldier, Urchin]
    '''
        backgrounds = {Acolyte.name: Acolyte, Charlatan.name: Charlatan, Criminal.name: Criminal,
                       Entertainer.name: Entertainer,
                       FolkHero.name: FolkHero, GuildArtisan.name: GuildArtisan, Hermit.name: Hermit, Noble.name: Noble,
                       Outlander.name: Outlander, Sage.name: Sage, Sailor.name: Sailor, Soldier.name: Soldier,
                       Urchin.name: Urchin}
                       '''


def reset_stats():
    for abil in Abilities.list:
        abil.score = 0
        abil.mod = 0
    pass


def recalc_mods():
    for abil in Abilities.list:
        abil.mod = math.floor((abil.score - 10) / 2)
    pass


def gen_backstory(character_object):
    try:
        f = open(wrkdir + "//" + backstories, 'r', encoding="utf8")
        c = f.read().replace("\n", " ")
        generator = markovify.Text(c, state_size=3)
        sentences = []

        while len(sentences) < 10:
            a_sentence = generator.make_sentence()
            if a_sentence != None and a_sentence not in sentences:
                sentences.append(a_sentence)
        return " ".join(sentences).replace("$NAME", character_object.name).replace("$MYCLASS",character_object.myclass.name).replace("$RACE", character_object.myrace.name).replace("$BACKGROUND", character_object.bground.name)

    except:
        return ""


def create_mapping(character_object):
    stats = character_object.stats
    saving_throws = character_object.get_saving_throws()
    skills = character_object.get_skills()
    print("Skills" + str(skills))
    mapping_keys = {
        "ClassLevel": character_object.myclass.name,
        "CharacterName": character_object.name,
        "Race": character_object.myrace.name,
        "Background": character_object.bground.name,
        "Alignment": character_object.get_alignment(),
        "STR": stats.STR.score,
        "ProfBonus": 2,
        "AC": character_object.ac,
        "Speed": 30,
        "STRmod": stats.STR.mod,
        "ST Strength": saving_throws["STR"],
        "DEX": stats.DEX.score,
        "DEXmod": stats.DEX.mod,
        "CON": stats.CON.score,
        "CONmod": stats.CON.mod,
        "INT": stats.INT.score,
        "ST Dexterity": saving_throws["DEX"],
        "ST Constitution": saving_throws["CON"],
        "ST Intelligence": saving_throws["INT"],
        "ST Wisdom": saving_throws["WIS"],
        "ST Charisma": saving_throws["CHA"],
        "INTmod": stats.INT.mod,
        "WIS": stats.WIS.score,
        "WISmod": stats.WIS.mod,
        "CHA": stats.CHA.score,
        "HPMax": character_object.hp,
        "CHamod": stats.CHA.mod,
        "Passive": character_object.passive_perc,
        "ProficienciesLang": character_object.get_language(),
        "GP": character_object.gp,
        "CharacterName 2": character_object.name,
        "Age": character_object.age,
        "Height": character_object.height,
        "Weight": character_object.weight,
        "Backstory": character_object.backstory,
        "Spells 1015": character_object.get_spell(),
        "Acrobatics": skills["Acrobatics"],
        "Survival": skills["Survival"],
        "Animal": skills["Animal Handling"],
        "Athletics": skills["Athletics"],
        "Deception": skills["Deception"],
        "History": skills["History"],
        "Insight": skills["Insight"],
        "Intimidation": skills["Intimidation"],
        "Performance": skills["Performance"],
        "Medicine": skills["Medicine"],
        "Stealth": skills["Stealth"],
        "Nature": skills["Nature"],
        "Persuasion": skills["Persuasion"],
        "Arcana": skills["Arcana"],
        "Perception": skills["Perception"],
        "SleightOfHand": skills["Sleight of Hand"],
        "Investigation": skills["Investigation"],
        "Religion": skills["Religion"]
    }
    '''
    extras = {
        "Acrobatics": skills["Acrobatics"],
        "Survival": skills["Survival"], 
        "Animal": skills["Animal Handling"],
        "Athletics": skills["Athletics"],
        "Deception": skills["Deception"],
        "History": skills["History"],
        "Insight": skills["Insight"],
        "Intimidation": skills["Intimidation"],
        "Performance": skills["Performance"],
        "Medicine": skills["Medicine"],
        "Stealth": skills["Stealth"],
        "Nature": skills["Nature"],
        "Persuasion": skills["Persuasion"],
        "Arcana": skills["Arcana"],
        "Perception": skills["Perception"],
        "SleightOfHand": skills["Sleight of Hand"],
    }
    '''
    print(mapping_keys)
    return mapping_keys


def checkbox_mapping(character_object):
    map = [skill.checkbox for skill in character_object.skills] + [skill.checkbox for skill in
                                                                   character_object.myclass.sav_throw]
    return map

def write(character_object,
          pdf_output=wrkdir + "//Outputs"):
    pdf_template = wrkdir + "//" + pdf_filename
    pdf_output = pdf_output + "/{}_{}_{}.pdf".format(character_object.name, character_object.myclass.name,
                                                     character_object.myrace.name)
    mapping = create_mapping(character_object)
    check_map = checkbox_mapping(character_object)
    template_pdf = pdfrw.PdfReader(pdf_template)
    ANNOT_KEY = '/Annots'
    ANNOT_FIELD_KEY = '/T'
    ANNOT_VAL_KEY = '/V'
    ANNOT_RECT_KEY = '/Rect'
    SUBTYPE_KEY = '/Subtype'
    WIDGET_SUBTYPE_KEY = '/Widget'
    # print(template_pdf)
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        for annotation in annotations:
            #print(annotation)
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    if key in mapping.keys():
                        annotation.update(pdfrw.PdfDict(V=str(mapping[key])))
                    elif "race" in key.lower():
                        annotation.update(pdfrw.PdfDict(V=str(mapping["Race"])))
                    elif "dexmod" in key.lower():
                        annotation.update(pdfrw.PdfDict(V=str(mapping["DEXmod"])))
                    elif "deception" in key.lower():
                        annotation.update(pdfrw.PdfDict(V=str(mapping["Deception"])))
                    elif "history" in key.lower():
                        annotation.update(pdfrw.PdfDict(V=str(mapping["History"])))
                    elif "investigation" in key.lower():
                        annotation.update(pdfrw.PdfDict(V=str(mapping["Investigation"])))
                    elif "perception" in key.lower():
                        annotation.update(pdfrw.PdfDict(V=str(mapping["Perception"])))
                    elif "religion" in key.lower():
                        annotation.update(pdfrw.PdfDict(V=str(mapping["Religion"])))
                    elif "sleightofhand" in key.lower():
                        annotation.update(pdfrw.PdfDict(V=str(mapping["SleightOfHand"])))
                    elif "stealth" in key.lower():
                        annotation.update(pdfrw.PdfDict(V=str(mapping["Stealth"])))
                    elif key in check_map:
                        enable_checkbox = list(annotation.AP.D)[-1]
                        annotation.update(pdfrw.PdfDict(V=enable_checkbox))



    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    pdfrw.PdfWriter().write(pdf_output, template_pdf)


class Char:
    def __init__(self) -> None:
        self.myrace = self.det_race()
        self.myclass = self.det_class()
        self.statsrank = self.rankedstats()
        self.stats = self.det_stats()
        self.profmod = 2
        self.bground = self.det_background()
        self.skills = self.bground.skill_prof
        self.passive_perc = self.det_passive_perc()
        self.name = self.det_name()
        x = self.det_h_w()
        self.height = x[0]
        self.weight = x[1]
        self.language = self.get_language()
        self.backstory = gen_backstory(self)
        self.gp = self.myclass.gold
        self.hp = self.det_hit_points()
        self.ac = self.gen_ac()
        self.age = self.get_age()


    def det_race(self):
        n = len(Race.list)
        race = Race.list[random.randint(0, n - 1)]
        try:
            m = len(race.subcat)
            race = race.subcat[random.randint(0, m - 1)]
        except AttributeError:
            pass
        return race

    def det_class(self):
        n = len(Class.list)
        char_class = Class.list[random.randint(0, n - 1)]
        return char_class

    def rankedstats(self):

        reset_stats()

        ranked_stats = {Abilities.STR: 0,
                        Abilities.DEX: 0,
                        Abilities.INT: 0,
                        Abilities.WIS: 0,
                        Abilities.CON: 0,
                        Abilities.CHA: 0}
        opposites = {Abilities.STR: Abilities.WIS,
                     Abilities.DEX: Abilities.CHA,
                     Abilities.INT: Abilities.STR,
                     Abilities.WIS: Abilities.STR,
                     Abilities.CON: Abilities.CHA,
                     Abilities.CHA: Abilities.DEX}

        for abil in self.myclass.prim_abil:
            ranked_stats[abil] += 3
        for abil in self.myclass.sav_throw:
            ranked_stats[abil] += 3

        for key in list(self.myrace.ability_score.keys()):
            ranked_stats[key] += self.myrace.ability_score[key]
            key.score += self.myrace.ability_score[key]

        for key in ranked_stats:
            opp = opposites[key]
            if ranked_stats[key] > 0 and ranked_stats[opp] == 0:
                ranked_stats[opp] = -(ranked_stats[key])
            else:
                pass

        return list({k: v for k, v in sorted(ranked_stats.items(), key=lambda item: item[1], reverse=True)}.keys())

    def det_stats(self):
        abilities = []
        for x in range(6):
            abilities.append(sum(sorted(roll_dice(d=6, num_dice=5, list=True))[:-2]))
        abilities = sorted(abilities)
        n = 0
        for abil in self.rankedstats():
            abil.score += abilities[n]
            n += 1
        recalc_mods()
        return Abilities

    def calc_factor(self, driver, driver_range):
        if driver < 6:
            factor = driver_range[0]
        elif driver > 15:
            factor = driver_range[1]
        else:
            factor = driver_range[0] + round(((driver - 5) / 10) * (driver_range[1] - driver_range[0]))
        return factor

    def det_h_w(self):
        h_mod = self.calc_factor(self.stats.STR.score, self.myrace.height_mod_ran)
        w_mod = self.calc_factor(self.stats.CON.score, self.myrace.weight_mod_ran)
        h_w = [(self.myrace.base_height + h_mod), self.myrace.base_weight + (h_mod * w_mod)]
        return [str(h_w[0] // 12) + "' " + str(h_w[0] % 12) + "\" ", str(h_w[1]) + "lbs."]

    def det_background(self):
        bground_scores = {}
        for bground in Backgrounds.bg_list:
            skill_sum = 0
            for skill in bground.skill_prof:
                skill_sum += skill.score.mod
            bground_scores[bground] = skill_sum
        char_bground = min(bground_scores, key=bground_scores.get)
        return char_bground

    def det_passive_perc(self):
        passive = 10 + self.stats.WIS.mod
        if Skills.Perception in self.skills:
            passive += self.profmod
        return passive

    def get_saving_throws(self):
        saving_throws = {"DEX": 0,
                         "CON": 0,
                         "INT": 0,
                         "WIS": 0,
                         "CHA": 0,
                         "STR": 0}

        for aclass in self.stats.list:
            saving_throws[aclass.name] = aclass.mod
        for aclass in self.myclass.sav_throw:
            saving_throws[aclass.name] += self.profmod
        return saving_throws

    def get_skills(self):
        skills = {
            "Acrobatics": 0,
            "Animal Handling": 0,
            "Arcana": 0,
            "Athletics": 0,
            "Deception": 0,
            "History": 0,
            "Insight": 0,
            "Intimidation": 0,
            "Investigation": 0,
            "Medicine": 0,
            "Nature": 0,
            "Perception": 0,
            "Performance": 0,
            "Persuasion": 0,
            "Religion": 0,
            "Sleight of Hand": 0,
            "Stealth": 0,
            "Survival": 0
        }
        for askill in Skills.list:
            skills[askill.name] = askill.score.mod
        for x in self.skills:
            skills[x.name] += self.profmod #self.skills[x].mod
        return skills

    def det_name(self):
        if self.myrace.name == "Elf, Wood":
            name = "Elle Woods"
        elif self.myrace.name == "Gnome, Forest":
            name = "Chad"
        elif self.bground.name == "Sage":
            name = "Dumbass"
        elif self.bground.name == "Acolyte":
            name = "ur mom"
        elif self.myclass.name == "Cleric":
            name = "Karen"
        else:
            name = str(uuid.uuid4())
        return name

    def get_language(self):
        languages = ["Abyssal", "Deep Speech", "Primordial", "Sylvan"]
        return languages[random.randint(0, len(languages) - 1)]

    def get_age(self):
        if self.myrace.max_age < 420:
            age = 69
        else:
            age = 420
        return age

    def get_spell(self):
        return "True Strike"

    def get_alignment(self):
        return "Chaotic Evil"

    def det_hit_points(self):
        con_modifier = self.stats.CON.mod
        base_8 = ["Bard", "Cleric", "Druid", "Monk", "Warlock"]
        base_10 = ["Fighter", "Paladin", "Ranger"]
        base_6 = ["Sorcerer", "Wizard"]
        base_12 = ["Barbarian"]
        class_name = self.myclass.name
        if class_name in base_8:
            return 8 + con_modifier
        elif class_name in base_10:
            return 10 + con_modifier
        elif class_name in base_6:
            return 6 + con_modifier
        elif class_name in base_12:
            return 12 + con_modifier
        else:
            return roll_dice(8, 1)
        pass

    def gen_ac(self):
        if (self.myclass == Class.Barbarian):
            return 10 + self.stats.DEX.mod + self.stats.CON.mod
        elif (self.myclass == Class.Monk):
            return 10 + self.stats.DEX.mod + self.stats.WIS.mod
        else:
            return 10 + self.stats.DEX.mod


for x in range(0, 10):
    character = Char()
    write(character)
