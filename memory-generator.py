import json
import re
import uuid

# warning. This will void your warranty. This will break your savegame.
# Specifically, this script exists to put entities in a very particular place and pattern. It will probably not work for your computer.
# Use it as reference, not as a thing to blindly run.

# credit to https://github.com/skysdottir/timberborn-map-editing

# Okay- the big one. Let's make some memories! This will be 13-29, inclusive, the addresses for which I already have read and write demuxes built for

print("Loading world...")

world = open("world-merged.json", "r")
jason = json.load(world)
entities = jason["Entities"]


def get_name(ent):
    return ent["Components"]["NamedEntity"]["EntityName"]

def is_relay(ent):
    return ent["Template"] == "Relay.Folktails"
    
rd_pattern = r"rd_([0-9]+)"
wd_pattern = r"wd_([0-9]+)"
bit_pattern = r"bit_([0-9]+)"
memo_pattern = r"memo_([0-9]+)_([0-9]+)"
mema_pattern = r"mema_([0-9]+)_([0-9]+)"

rds = {}
wds = {}
bits = {}
memos = {}
memas = {}

print("Finding existing relays")

rels = filter(is_relay, entities)

for relay in rels:
    name = get_name(relay)
    
    is_rd = re.search(rd_pattern, name)
    if(is_rd != None):
        rds[int(is_rd.group(1))]=relay
        
    is_wd = re.search(wd_pattern, name)
    if(is_wd != None):
        wds[int(is_wd.group(1))]=relay
    
    is_bit = re.search(bit_pattern, name)
    if(is_bit != None):
        bits[int(is_bit.group(1))]=relay
    
    is_memo = re.search(memo_pattern, name)
    if(is_memo != None):
        addr = int(is_memo.group(1))
        bit = int(is_memo.group(2))
        
        if(memos.get(addr) == None):
            memos[addr] = {}
        
        memos[addr][bit]=relay

    is_mema = re.search(mema_pattern, name)
    if(is_mema != None):
        memas[int(is_mema.group(1))]=relay

print("Found rds: " + str(len(rds)))
print("Found wds: " + str(len(wds)))
print("Found bits: " + str(len(bits)))
print("Found existing memos: " + str(len(memos)))

for addr in range(13,30):
    print("Generating cells for address " + str(addr))
    memos[addr]={}
    
    for bit in range(16):
        
        addz = str(addr)
        bitz = str(bit)
        bonus =  2 if (bit > 7) else 0
        
        mem_id = str(uuid.uuid4())
        mem = {"Id":mem_id,"Template":"Memory.Folktails","Components":{"NamedEntity":{"EntityName":"mem_" + addz + "_" + bitz},"BlockObject":{"Coordinates":{"X":76+(4*bit)+bonus,"Y":255-addr,"Z":4}},"Memory":{"Mode":"FlipFlop","InputA":bits[bit]["Id"] ,"InputB":wds[addr]["Id"]},"Automator":{"State":"Off"},"Inventory:ConstructionSite":{"Storage":{"Goods":[{"Good":"MetalBlock","Amount":1},{"Good":"Extract","Amount":1}]}}}}
        
        mema_id = str(uuid.uuid4())
        mema = {"Id":mema_id,"Template":"Relay.Folktails","Components":{"NamedEntity":{"EntityName":"mema_" + addz + "_" + bitz},"BlockObject":{"Coordinates":{"X":75+(4*bit)+bonus,"Y":255-addr,"Z":4}},"Relay":{"Mode":"And","InputA":mem_id,"InputB":rds[addr]["Id"]},"Automator":{"State":"Off"},"Inventory:ConstructionSite":{"Storage":{"Goods":[{"Good":"Plank","Amount":1},{"Good":"Gear","Amount":1}]}}}}
        
        memo = {"Id":str(uuid.uuid4()),"Template":"Relay.Folktails","Components":{"NamedEntity":{"EntityName":"memo_" + addz + "_" + bitz},"BlockObject":{"Coordinates":{"X":74+(4*bit)+bonus,"Y":255-addr,"Z":4}},"Relay":{"Mode":"Or","InputA":memos[addr-1][bit]["Id"],"InputB":mema_id},"Automator":{"State":"Off"},"Inventory:ConstructionSite":{"Storage":{"Goods":[{"Good":"Plank","Amount":1},{"Good":"Gear","Amount":1}]}}}}
        
        entities.append(mem)
        entities.append(mema)
        entities.append(memo)
        
        memos[addr][bit] = memo

print("Writing output world")

out = open("out-generated-world.json", "w")
json.dump(jason, out)