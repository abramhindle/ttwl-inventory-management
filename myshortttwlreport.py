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
    args = parser.parse_args()
    for filename in args.filenames:
        out = parse_and_report(filename)
        print(",".join([str(x) for x in out]))

def parse_and_report(filename,parts=False,annoints=False):
    save = TTWLSave(filename)
    bfilename = os.path.basename(filename)
    out = [bfilename,save.get_char_name(), str(save.get_savegame_id()),save.get_primary_class(True),save.get_secondary_class(True),save.get_pt_mayhem_level(0)]
    return out

if __name__ == '__main__':
    main()
