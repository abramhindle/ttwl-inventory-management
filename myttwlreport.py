#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright (c) 2020 CJ Kucera (cj@apocalyptech.com)
# 
# This software is provided 'as-is', without any express or implied warranty.
# In no event will the authors be held liable for any damages arising from
# the use of this software.
# 
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software in a
#    product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 
# 3. This notice may not be removed or altered from any source distribution.

import ttwlsave
import argparse
import itertools
from ttwlsave.ttwlsave import TTWLSave
import os

seperator = "|"

_extraNames = [
    (r'Part_Ability_VictoryRush','VictoryRush'),
    (r'Artifact_Part_Ability_Snowdrift','Snowdrift'),
    (r'OttoIdol','OttoIdol'),
    (r'FastHands','Cutpurse'),
    (r'Artifact_Part_Ability_Salvo','Launchpad'),
    (r'ElementalOrigin','ElementalProjector'),
    (r'WhiteElephant','WhiteElephant'),
    (r'FireStone','FireStone'),
    (r'ShockStone','ShockStone'),
    (r'RocketBoots','RocketBoots'),
    (r'Deathless','Deathless'),
    (r'LastStand','LastStand'),
    (r'IceSpiker','IceSpiker'),
    (r'SplatterGun','SplatterGun'),
    (r'KnifeDrain','KnifeDrain'),
    (r'MoxxisEndowment','MoxxisEndowment'),
    (r'LootExpander','LootExpanding'),
    (r'CorrosiveStone','CorrosiveStone'),
    (r'CryoStone','CyroStone'),
    (r'RadiationStone','RadiationStone'),
    (r'CosmicCrater','CosmicCrater'),
    (r'SafeGuard','SafeGuard'),
    (r'Safeguard','Safeguard'),
    (r'Safegaurd','Safeguard'),
    (r'AtomBalm','AtomBalm'),
    (r'CommanderPlanetoid','CommanderPlanetoid'),
    (r'BloodFrenzy','BloodFrenzy?'),
    (r'RearEnder','RearEnder'),
    (r'CausticCoast','CausticCoast'),
    (r'PullOutMethod','PullOutMethod'),
    (r'HotDrop','HotDrop'),
    (r'StaticTouch','Shockslide?'),
    (r'ToxicRevenger','ToxicRevenge?'),
    (r'ShatterRig','ShatterRig?'),
    (r'LoadedDice','LoadedDice'),
    (r'FleshMelter','FleshMelter'),
]   

def extraName(item):
    v = item.balance
    parts = item._parts
    if parts is None or len(parts) < 1:
        return ""
    part_names = [y[0] for y in parts]
    out = []
    for part_name in part_names:
        for en in _extraNames:
            if en[0] in part_name:
                out.insert(0,en[1])
    return " ".join(out)

def getAnnoint(x,all=False):
    try:
        v = x.balance
        parts = x._generic_parts
        if (len(parts) <= 0):
            return ""
        if (all):
            return ", ".join([y[0] for y in parts])
        else:
            return parts[0][0]
    except:
        return ""

def getParts(x):
    try:
        v = x.balance
        parts = x._parts
        if (len(parts) <= 0):
            return ""
        return ", ".join([y[0] for y in parts])
    except:
        return ""

def reportItem(item,parts=False,annoints=False):
    if item is None:
        return seperator.join(['None',"","","",""])
    if item.eng_name:
        partstr = ""
        if parts:
            partstr = getParts(item)
        return seperator.join(
                [str(x) for x in 
                    [" ".join([item.eng_name,extraName(item)]).strip(), 
                     item.get_level_eng(), 
                     getAnnoint(item,all=annoints), 
                     partstr, 
                     item.get_serial_base64()]])
    else:
        return seperator.join([str(x) for x in ['unknown item',"","","",item.get_serial_base64()]])

def main():

    # Arguments
    parser = argparse.ArgumentParser(
            description='Wonderlands Savegame Info Dumper v{}'.format(ttwlsave.__version__),
            )

    parser.add_argument('filenames',
            nargs='+',
            help='Filenames to process',
            )
    parser.add_argument('--parts',
            default=False,
            action='store_true',
            help='show parts',
            )
    parser.add_argument('--annoints',
            default=False,
            action='store_true',
            help='show all annoints',
            )

    args = parser.parse_args()
    for filename in args.filenames:
        parse_and_report(filename,args.parts,args.annoints)
    # Load the save

def parse_and_report(filename,parts=False,annoints=False):
    save = TTWLSave(filename)
    bfilename = os.path.basename(filename)
    out = [bfilename,save.get_char_name(), str(save.get_savegame_id()),save.get_primary_class(True),save.get_secondary_class(True)]

    # Inventory
    items = save.get_items()
    if len(items) > 0:
        to_report = []
        for item in items:
            to_report.append( reportItem( item, parts=parts, annoints=annoints ))
            #if item.eng_name:
            #    partstr = ""
            #    if parts:
            #        partstr = getParts(item)
            #    to_report.append('{}|{}|{}|{}|{}'.format(item.eng_name, item.get_level_eng(), getAnnoint(item,all=annoints), partstr, item.get_serial_base64()))
            #else:
            #    to_report.append(' - unknown item: {}'.format(item.get_serial_base64()))
        for line in sorted(to_report):
            print(seperator.join([line]+out))

    # Equipped Items
    items = save.get_equipped_items(True)
    if any(items.values()):
        to_report = []
        for (slot, item) in items.items():
            to_report.append( reportItem( item, parts=parts, annoints=annoints ))
            #if item:
            #    if item.eng_name:
            #        to_report.append(' - {} ({}): {} {}'.format(item.eng_name, item.get_level_eng(), getAnnoint(item,all=annoints), item.get_serial_base64()))
            #    else:
            #        to_report.append(' - {}: unknown item: {}'.format(slot, item.get_serial_base64()))
        for line in sorted(to_report):
            print(seperator.join([line]+out))


if __name__ == '__main__':
    main()
