import json
import re
import uuid

world_file = open("saves/_template_world.json")
world = json.load(world_file)

print("world loaded")
print("Game Version ", world["GameVersion"])
print("Map Size ", world["Singletons"]["MapSize"]["Size"])

entities = world["Entities"]

# Naming patterns

ind_pattern = r"([0-9]+)_([0-9]+)_IND_([0-9]+)"
mem_pattern = r"([0-9]+)_([0-9]+)_MEM"
and_pattern = r"([0-9]+)_([0-9]+)_AND_([0-9]+)"
or_pattern = r"([0-9]+)_([0-9]+)_OR_([0-9]+)"
not_pattern = r"([0-9]+)_([0-9]+)_NOT_([0-9]+)"

def is_platform(ent):
    return ent["Template"] == "DoublePlatform.IronTeeth"

def get_coords(ent):
    x = ent["Components"]["BlockObject"]["Coordinates"]["X"]
    y = ent["Components"]["BlockObject"]["Coordinates"]["Y"]
    z = ent["Components"]["BlockObject"]["Coordinates"]["Z"]
    
    return ({x,y,z})

existing_platforms = filter(is_platform, entities)

def has_platform(x, y, z):
    for e in existing_platforms:
        if (get_coords(e) == {x, y, z}):
            return (1)
    return (0)

def generate_platform(x, y, z):
    id = str(uuid.uuid4())
    
    return({"Id": id,"Template": "DoublePlatform.IronTeeth","Components": {"BlockObject": {"Coordinates": {"X": x,"Y": y,"Z": z},"Orientation": "Cw90"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 8}]}}}})

def place_tower(px, py):
    for z in range(12):
        for x in range(2):
            for y in range(2):
                if (has_platform(px + x, py + y, z * 2)):
                    continue
                new_platform = generate_platform(px + x, py + y, z * 2)
                # existing_platforms.append(new_platform)
                entities.append(new_platform)

true = True
false = False


lev_reset   = {"Id": str(uuid.uuid4()),"Template": "Lever.IronTeeth","Components": {"NamedEntity": {"EntityName": "Global Reset"},"BlockObject": {"Coordinates": {"X": 8,"Y": 8,"Z": 0},"Orientation": "Cw270"},"Lever": {"IsSpringReturn": true},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 2}]}}}}
sim_control = {"Id": str(uuid.uuid4()),"Template": "Lever.IronTeeth","Components": {"NamedEntity": {"EntityName": "Sim  Control"},"BlockObject": {"Coordinates": {"X": 9,"Y": 9,"Z": 0},"Orientation": "Cw270"},"Lever": {"IsSpringReturn": false},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 2}]}}}}
clock       = {"Id": str(uuid.uuid4()),"Template": "Timer.IronTeeth","Components": {"NamedEntity": {"EntityName": "Simul  Clock"},"BlockObject": {"Coordinates": {"X": 10,"Y": 10,"Z": 0},"Orientation": "Cw270"},"Timer": {"Mode": "Oscillator","TimerIntervalA": {"Ticks": 1},"TimerIntervalB": {"Type": "Hours","Hours": 1.0},"Input": sim_control["Id"],"PreviousInputState": true,"Counter": 6},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "TreatedPlank","Amount": 1},{"Good": "MetalBlock","Amount": 1}]}}}}

entities.append(lev_reset)
entities.append(sim_control)
entities.append(clock)

cell_table = {}
control_ORs = {}
def place_memory(px, py):
    lev_set     = {"Id": str(uuid.uuid4()),"Template": "Lever.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_LEV_ON"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py,"Z": 20},"Orientation": "Cw270"},"Lever": {"IsSpringReturn": true},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 2}]}}}}
    or_set      = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_10_1"},"BlockObject": {"Coordinates": {"X": px,"Y": py,"Z": 20},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": lev_set["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    or_reset    = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_10_2"},"BlockObject": {"Coordinates": {"X": px,"Y": py + 1,"Z": 20},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": lev_reset["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}

#   in or set and or reset input B was removed and needs to be addedmanually once it exists. we need to find them. thats why we store them in a table
    control_ORs.update({or_set["Components"]["NamedEntity"]["EntityName"]: or_set})
    control_ORs.update({or_reset["Components"]["NamedEntity"]["EntityName"]: or_reset})

    cell = {"Id": str(uuid.uuid4()),"Template": "Memory.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_MEM"},"BlockObject": {"Coordinates": {"X": px,"Y": py + 1,"Z": 18}},"Memory": {"Mode": "SetReset","InputA": or_set["Id"],"ResetInput": or_reset["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "MetalBlock","Amount": 1},{"Good": "Extract","Amount": 1}]}}}}
    cell_table.update({cell["Components"]["NamedEntity"]["EntityName"]: cell["Id"]})


    ind1 = {"Id": str(uuid.uuid4()),"Template": "Indicator.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_IND_10"},"BlockObject": {"Coordinates": {"X": px,"Y": py,"Z": 24}},"Indicator": {},"Automatable": {"Input": cell["Id"]},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "ScrapMetal","Amount": 1},{"Good": "PineResin","Amount": 1}]}}}}
    ind2 = {"Id": str(uuid.uuid4()),"Template": "Indicator.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_IND_11"},"BlockObject": {"Coordinates": {"X": px,"Y": py + 1,"Z": 24}},"Indicator": {},"Automatable": {"Input": cell["Id"]},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "ScrapMetal","Amount": 1},{"Good": "PineResin","Amount": 1}]}}}}
    ind3 = {"Id": str(uuid.uuid4()),"Template": "Indicator.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_IND_12"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py,"Z": 24}},"Indicator": {},"Automatable": {"Input": cell["Id"]},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "ScrapMetal","Amount": 1},{"Good": "PineResin","Amount": 1}]}}}}
    ind4 = {"Id": str(uuid.uuid4()),"Template": "Indicator.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_IND_13"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py + 1,"Z": 24}},"Indicator": {},"Automatable": {"Input": cell["Id"]},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "ScrapMetal","Amount": 1},{"Good": "PineResin","Amount": 1}]}}}}

    entities.append(lev_set)
    entities.append(or_set)
    entities.append(or_reset)
    entities.append(cell)
    entities.append(ind1)
    entities.append(ind2)
    entities.append(ind3)
    entities.append(ind4)

def find_mem(px, py):
    name = str(px) + "_" + str(py) + "_MEM"
    for c in cell_table:
        if c == name:
            return cell_table[c]
    print("Could not find memory at " + name)
    return lev_reset["Id"]

def update_control_OR(px, py, type, input_b):
    name = str(px) + "_" + str(py) + "_OR_10_"
    if type == "set":
        name += "1"
    else:
        name += "2"
    
    for c in control_ORs:
        if c == name:
            control_ORs[c]["Components"]["Relay"].update({"InputB": input_b})
            return
    print ("debug")


def place_logic(px, py):
    and1_1 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_AND_1_1"},"BlockObject": {"Coordinates": {"X": px,"Y": py + 1,"Z": 0},"Orientation": "Cw270"},"Relay": {"Mode": "And","InputA": find_mem(px - 2, py - 2),"InputB": find_mem(px, py - 2)},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    and1_2 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_AND_1_2"},"BlockObject": {"Coordinates": {"X": px,"Y": py,"Z": 0},"Orientation": "Cw270"},"Relay": {"Mode": "And","InputA": find_mem(px + 2, py - 2),"InputB": find_mem(px + 2, py)},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    and1_3 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_AND_1_3"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py,"Z": 0},"Orientation": "Cw270"},"Relay": {"Mode": "And","InputA": find_mem(px + 2, py + 2),"InputB": find_mem(px, py + 2)},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    and1_4 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_AND_1_4"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py + 1,"Z": 0},"Orientation": "Cw270"},"Relay": {"Mode": "And","InputA": find_mem(px - 2, py + 2),"InputB": find_mem(px - 2, py)},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}

    or1_1 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_1_1"},"BlockObject": {"Coordinates": {"X": px,"Y": py + 1,"Z": 2},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": find_mem(px - 2, py - 2),"InputB": find_mem(px, py - 2)},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    or1_2 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_1_2"},"BlockObject": {"Coordinates": {"X": px,"Y": py,"Z": 2},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": find_mem(px + 2, py - 2),"InputB": find_mem(px + 2, py)},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    or1_3 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_1_3"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py,"Z": 2},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": find_mem(px + 2, py + 2),"InputB": find_mem(px, py + 2)},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    or1_4 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_1_4"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py + 1,"Z": 2},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": find_mem(px - 2, py + 2),"InputB": find_mem(px - 2, py)},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}} 

    and2_1 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_AND_2_1"},"BlockObject": {"Coordinates": {"X": px,"Y": py + 1,"Z": 4},"Orientation": "Cw270"},"Relay": {"Mode": "And","InputA": and1_1["Id"],"InputB": and1_2["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    and2_2 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_AND_2_2"},"BlockObject": {"Coordinates": {"X": px,"Y": py,"Z": 4},"Orientation": "Cw270"},"Relay": {"Mode": "And","InputA": or1_1["Id"],"InputB": or1_2["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    and2_3 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_AND_2_3"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py,"Z": 4},"Orientation": "Cw270"},"Relay": {"Mode": "And","InputA": and1_3["Id"],"InputB": and1_4["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    and2_4 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_AND_2_4"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py + 1,"Z": 4},"Orientation": "Cw270"},"Relay": {"Mode": "And","InputA": or1_3["Id"],"InputB": or1_4["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}

    or2_1 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_2_1"},"BlockObject": {"Coordinates": {"X": px,"Y": py + 1,"Z": 6},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": and1_1["Id"],"InputB": and1_2["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    or2_2 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_2_2"},"BlockObject": {"Coordinates": {"X": px,"Y": py,"Z": 6},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": or1_1["Id"],"InputB": or1_2["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    or2_3 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_2_3"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py,"Z": 6},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": and1_3["Id"],"InputB": and1_4["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    or2_4 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_2_4"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py + 1,"Z": 6},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": or1_3["Id"],"InputB": or1_4["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}

    and3_1 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_AND_3_1"},"BlockObject": {"Coordinates": {"X": px,"Y": py + 1,"Z": 8},"Orientation": "Cw270"},"Relay": {"Mode": "And","InputA": or2_1["Id"],"InputB": and2_2["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    and3_2 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_AND_3_2"},"BlockObject": {"Coordinates": {"X": px,"Y": py,"Z": 8},"Orientation": "Cw270"},"Relay": {"Mode": "And","InputA": or2_3["Id"],"InputB": and2_4["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    or3_1 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_3_1"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py,"Z": 8},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": or2_1["Id"],"InputB": and2_2["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    or3_2 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_3_2"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py + 1,"Z": 8},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": or2_3["Id"],"InputB": and2_4["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}

    or4_1 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_4_1"},"BlockObject": {"Coordinates": {"X": px,"Y": py + 1,"Z": 10},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": and2_1["Id"],"InputB": and2_3["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    or4_2 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_4_2"},"BlockObject": {"Coordinates": {"X": px,"Y": py,"Z": 10},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": and3_1["Id"],"InputB": and3_2["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    and4_1 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_AND_4_1"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py,"Z": 10},"Orientation": "Cw270"},"Relay": {"Mode": "And","InputA": or3_1["Id"],"InputB": or3_2["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    or4_3 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_4_3"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py + 1,"Z": 10},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": or3_1["Id"],"InputB": or3_2["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}

    and4_2 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_AND_4_2"},"BlockObject": {"Coordinates": {"X": px,"Y": py + 1,"Z": 12},"Orientation": "Cw270"},"Relay": {"Mode": "And","InputA": or2_2["Id"],"InputB": or2_4["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    or5_1 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_5_1"},"BlockObject": {"Coordinates": {"X": px,"Y": py,"Z": 12},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": or4_1["Id"],"InputB": and4_1["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    and5_1 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_AND_5_1"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py,"Z": 12},"Orientation": "Cw270"},"Relay": {"Mode": "And","InputA": or4_2["Id"],"InputB": and4_2["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    or5_2 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_5_2"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py + 1,"Z": 12},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": or4_2["Id"],"InputB": and4_2["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}

    or6_1 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_6_1"},"BlockObject": {"Coordinates": {"X": px,"Y": py + 1,"Z": 14},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": or5_1["Id"],"InputB": and5_1["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    and6_1 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_AND_6_1"},"BlockObject": {"Coordinates": {"X": px,"Y": py,"Z": 14},"Orientation": "Cw270"},"Relay": {"Mode": "And","InputA": or5_2["Id"],"InputB": or4_3["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    or6_2 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_6_2"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py,"Z": 14},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": or5_2["Id"],"InputB": or4_3["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    not6_1 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_NOT_6_1"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py + 1,"Z": 14},"Orientation": "Cw270"},"Relay": {"Mode": "Not","InputA": or6_1["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}

    and7_1 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_AND_7_1"},"BlockObject": {"Coordinates": {"X": px,"Y": py + 1,"Z": 16},"Orientation": "Cw270"},"Relay": {"Mode": "And","InputA": or6_2["Id"],"InputB": find_mem(px, py)},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    or7_1 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_OR_7_1"},"BlockObject": {"Coordinates": {"X": px,"Y": py,"Z": 16},"Orientation": "Cw270"},"Relay": {"Mode": "Or","InputA": and7_1["Id"],"InputB": and6_1["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    and7_2 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_AND_7_2"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py,"Z": 16},"Orientation": "Cw270"},"Relay": {"Mode": "And","InputA": or7_1["Id"],"InputB": not6_1["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    not7_1 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_NOT_7_1"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py + 1,"Z": 16},"Orientation": "Cw270"},"Relay": {"Mode": "Not","InputA": and7_2["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}

    and8_1 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_AND_8_1"},"BlockObject": {"Coordinates": {"X": px,"Y": py,"Z": 18},"Orientation": "Cw270"},"Relay": {"Mode": "And","InputA": clock["Id"],"InputB": and7_2["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    and8_2 = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_AND_8_2"},"BlockObject": {"Coordinates": {"X": px + 1,"Y": py,"Z": 18},"Orientation": "Cw270"},"Relay": {"Mode": "And","InputA": clock["Id"],"InputB": not7_1["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    update_control_OR(px, py, "set", and8_1["Id"])
    update_control_OR(px, py, "reset", and8_2["Id"])



    entities.append(and1_1)
    entities.append(and1_2)
    entities.append(and1_3)
    entities.append(and1_4)
    entities.append(or1_1)
    entities.append(or1_2)
    entities.append(or1_3)
    entities.append(or1_4)
    entities.append(and2_1)
    entities.append(and2_2)
    entities.append(and2_3)
    entities.append(and2_4)
    entities.append(or2_1)
    entities.append(or2_2)
    entities.append(or2_3)
    entities.append(or2_4)
    entities.append(and3_1)
    entities.append(and3_2)
    entities.append(or3_1)
    entities.append(or3_2)
    entities.append(or4_1)
    entities.append(or4_2)
    entities.append(and4_1)
    entities.append(or4_3)
    entities.append(and4_2)
    entities.append(or5_1)
    entities.append(and5_1)
    entities.append(or5_2)
    entities.append(or6_1)
    entities.append(and6_1)
    entities.append(or6_2)
    entities.append(not6_1)
    entities.append(and7_1)
    entities.append(or7_1)
    entities.append(and7_2)
    entities.append(not7_1)
    entities.append(and8_1)
    entities.append(and8_2)


world_x =  world["Singletons"]["MapSize"]["Size"]["X"]
world_y =  world["Singletons"]["MapSize"]["Size"]["Y"]

def build_grid():
    cells_x = 30
    cells_y = 30

    start_x = 20
    start_y = 20

    for x in range(1, cells_x + 1):
        for y in range(1, cells_y + 1):
            place_tower(start_x + x * 2, start_y + y * 2)
            place_memory(start_x + x * 2, start_y + y * 2)
    
    for x in range(2, cells_x):
        for y in range(2, cells_y):
            place_logic(start_x + x * 2, start_y + y * 2)

build_grid()

def test():
    cell = {"Id": str(uuid.uuid4()),"Template": "Memory.IronTeeth","Components": {"NamedEntity": {"EntityName": str(33) + "_" + str(33) + "_MEM"},"BlockObject": {"Coordinates": {"X": 33,"Y": 33 + 1,"Z": 18}},"Memory": {"Mode": "SetReset"},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "MetalBlock","Amount": 1},{"Good": "Extract","Amount": 1}]}}}}
    cell_table.update({cell["Components"]["NamedEntity"]["EntityName"]: cell["Id"]})
    cell_table.update({"42_42_MEM": "test"})
    print(cell_table)
    find_mem(33, 33)

# test()

out = open("saves/world.json", "w")
json.dump(world, out)
