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

def parts(item):
    print(item.eng_name)
    print(sorted([x[0] for x in item._parts]))
