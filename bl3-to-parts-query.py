from ttwlsave import datalib
from ttwlsave.datalib import DataWrapper
from ttwlsave.ttwlsave import BL3Item
import csv
from collections import Counter

BL3COL = 2
DW = DataWrapper()

def create_item(item_serial_b64):
    new_item = BL3Item.create(DW, 
        serial_number=datalib.BL3Serial.decode_serial_base64(item_serial_b64),
        pickup_order_idx=666,
        is_favorite=False,
    )
    return new_item

def blfilter(item):
    eng = item.eng_name
    # if eng != "Balance_Armor_CapeOfTides":
    #    return False
    parts = item._parts
    if parts is None:
        return False
    ranger_parts = filter(lambda x: "Ranger" in x[0] , parts)
    if len(list(ranger_parts)) < 1:
        return False
    skill_parts = filter(lambda x: "SkillParts" in x[0] , parts)
    c = Counter()
    c.update( skill_parts )
    for elm in c:
        if c[elm] >= 3:
            return True
    return False



with open('ttwl-everyitem.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    rows = [row for row in reader]
    # items = []
    for row in rows:
        # print(row)
        if len(row[BL3COL]):
            item = create_item(row[BL3COL])
            eng = item.eng_name
            # items.append( item )
            if blfilter(item):
                s = ",".join([eng,str(item._parts),item.get_serial_base64(),str(item._item_type)])
                print(s)
    # # items = [create_item(row[BL3COL]) for row in rows]
    # for item in items:
    #     eng = item.eng_name
    #     s = ",".join([eng,str(item._parts),item.get_serial_base64(),str(item._item_type)])
    #     print(s)

