from ttwlsave import datalib
from ttwlsave.datalib import DataWrapper
from ttwlsave.ttwlsave import BL3Item
import csv

BL3COL = 2
DW = DataWrapper()

def create_item(item_serial_b64):
    new_item = BL3Item.create(DW, 
        serial_number=datalib.BL3Serial.decode_serial_base64(item_serial_b64),
        pickup_order_idx=666,
        is_favorite=False,
    )
    return new_item

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
            s = ",".join([eng,str(item._parts),item.get_serial_base64(),str(item._item_type)])
            print(s)
    # # items = [create_item(row[BL3COL]) for row in rows]
    # for item in items:
    #     eng = item.eng_name
    #     s = ",".join([eng,str(item._parts),item.get_serial_base64(),str(item._item_type)])
    #     print(s)

