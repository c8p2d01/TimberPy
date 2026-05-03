import json
import time
import uuid

world_file = open("saves/_template_world.json")
world = json.load(world_file)

print("world loaded")
print("Game Version ", world["GameVersion"])
print("Map Size ", world["Singletons"]["MapSize"]["Size"])

entities = world["Entities"]

def is_platform(ent):
    return ent["Template"] == "DoublePlatform.IronTeeth"

def get_coords(ent):
    x = ent["Components"]["BlockObject"]["Coordinates"]["X"]
    y = ent["Components"]["BlockObject"]["Coordinates"]["Y"]
    z = ent["Components"]["BlockObject"]["Coordinates"]["Z"]
    
    return ({x,y,z})

existing_platforms = [e for e in entities if is_platform(e)]

def has_platform(x, y, z):
    for e in existing_platforms:
        if (get_coords(e) == {x, y, z}):
            return (1)
    return (0)

def generate_platform(x, y, z):
    id = str(uuid.uuid4())
    return({"Id": id,"Template": "DoublePlatform.IronTeeth","Components": {"BlockObject": {"Coordinates": {"X": x,"Y": y,"Z": z},"Orientation": "Cw90"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 8}]}}}})

def generate_memory(px, py, pz, name, set, reset):
    return ({"Id": str(uuid.uuid4()),"Template": "Memory.IronTeeth","Components": {"NamedEntity": {"EntityName": name},"BlockObject": {"Coordinates": {"X": px,"Y": py,"Z": pz}},"Memory": {"Mode": "SetReset","InputA": set,"ResetInput": reset},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "MetalBlock","Amount": 1},{"Good": "Extract","Amount": 1}]}}}})

def generate_relay(px, py, pz, name, r_type, inputA, inputB):
    return ({"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": name},"BlockObject": {"Coordinates": {"X": px,"Y": py,"Z": pz}},"Relay": {"Mode": r_type,"InputA": inputA,"InputB": inputB},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}})

def generate_denial(px, py, pz, name, inputA):
    return ({"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": name},"BlockObject": {"Coordinates": {"X": px,"Y": py,"Z": pz}},"Relay": {"Mode": "Not","InputA": inputA},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}})

def generate_lamp(px, py, pz, input):
    return ({"Id": str(uuid.uuid4()),"Template": "Indicator.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "_" + str(pz) + "Lamp"},"BlockObject": {"Coordinates": {"X": px,"Y": py,"Z": pz}},"Indicator": {},"Automatable": {"Input": input},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "ScrapMetal","Amount": 1},{"Good": "PineResin","Amount": 1}]}}}}) 

def place_tower(px, py):
    for z in range(16):
        new_platform = generate_platform(px, py, z * 2)
        entities.append(new_platform)

def get_by_name(set, name): 
    for e in set:
        named = e.get("Components", {}).get("NamedEntity")
        if named and named.get("EntityName") == name:
            return e
    return None

def set_InputA(e, new_id):
    mode = e.get("Components", {}).get("Relay")
    if (mode == None):
        return
    mode["InputA"] = new_id

def set_InputB(e, new_id):
    mode = e.get("Components", {}).get("Relay")
    if (mode == None):
        return
    mode["InputB"] = new_id

def set_Set(e, new_id):
    mode = e.get("Components", {}).get("Memory")
    if (mode == None):
        return
    mode["InputA"] = new_id

def set_Reset(e, new_id):
    mode = e.get("Components", {}).get("Memory")
    if (mode == None):
        print("err")
        return
    mode["ResetInput"] = new_id

true = True
false = False
grid_x = 12
grid_y = 12
offfset_x = 10
offfset_y = 10

food_flag = {"Id": str(uuid.uuid4()),"Template": "PowerMeter.IronTeeth","Components": {"NamedEntity": {"EntityName": "food_flag"},"BlockObject": {"Coordinates": {"X": 8,"Y": 0,"Z": 0},"Orientation": "Cw270"},"PowerMeter": {"Mode": "BatteryChargeLevel","ComparisonMode": "Greater","IntThreshold": 0,"PercentThreshold": 0.5},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Gear","Amount": 10},{"Good": "MetalBlock","Amount": 6}]}}}}
sim_control = {"Id": str(uuid.uuid4()),"Template": "Lever.IronTeeth","Components": {"NamedEntity": {"EntityName": "Sim  Control"},"BlockObject": {"Coordinates": {"X": 0,"Y": 0,"Z": 0},"Orientation": "Cw270"},"Lever": {"IsSpringReturn": false,"IsPinned": true},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 2}]}}}}
clock       = {"Id": str(uuid.uuid4()),"Template": "Timer.IronTeeth","Components": {"NamedEntity": {"EntityName": "Simul  Clock"},"BlockObject": {"Coordinates": {"X": 1,"Y": 1,"Z": 0},"Orientation": "Cw270"},"Timer": {"Mode": "Oscillator","TimerIntervalA": {"Ticks": 1},"TimerIntervalB": {"Type": "Hours","Hours": 1.0},"Input": sim_control["Id"],"PreviousInputState": true,"Counter": 6},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "TreatedPlank","Amount": 1},{"Good": "MetalBlock","Amount": 1}]}}}}
entities.append(sim_control)
entities.append(clock)
entities.append(food_flag)

temp = {"Id": str(uuid.uuid4()),"Template": "Lever.IronTeeth","Components": {"NamedEntity": {"EntityName": "placeholder_input"},"BlockObject": {"Coordinates": {"X": 0,"Y": 0,"Z": 0},"Orientation": "Cw270"},"Lever": {"IsSpringReturn": false,"IsPinned": true},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 2}]}}}}

def create_controls():
    Num_up = {"Id": str(uuid.uuid4()),"Template": "Lever.IronTeeth","Components": {"NamedEntity": {"EntityName": "aNum_up"},"BlockObject": {"Coordinates": {"X": 1,"Y": 2,"Z": 0},"Orientation": "Cw270"},"Lever": {"IsSpringReturn": true, "IsPinned": true},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 2}]}}}}
    Num_down = {"Id": str(uuid.uuid4()),"Template": "Lever.IronTeeth","Components": {"NamedEntity": {"EntityName": "cNum_down"},"BlockObject": {"Coordinates": {"X": 1,"Y": 0,"Z": 0},"Orientation": "Cw270"},"Lever": {"IsSpringReturn": true, "IsPinned": true},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 2}]}}}}
    Num_right = {"Id": str(uuid.uuid4()),"Template": "Lever.IronTeeth","Components": {"NamedEntity": {"EntityName": "dNum_right"},"BlockObject": {"Coordinates": {"X": 0,"Y": 1,"Z": 0},"Orientation": "Cw270"},"Lever": {"IsSpringReturn": true, "IsPinned": true},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 2}]}}}}
    Num_left = {"Id": str(uuid.uuid4()),"Template": "Lever.IronTeeth","Components": {"NamedEntity": {"EntityName": "bNum_left"},"BlockObject": {"Coordinates": {"X": 2,"Y": 1,"Z": 0},"Orientation": "Cw270"},"Lever": {"IsSpringReturn": true, "IsPinned": true},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 2}]}}}}
    entities.append(Num_up)
    entities.append(Num_down)
    entities.append(Num_right)
    entities.append(Num_left)
    Control_reset_V = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": "Control_reset_V"},"BlockObject": {"Coordinates": {"X": 2,"Y": 0,"Z": 0}},"Relay": {"Mode": "Or","InputA": Num_down["Id"],"InputB": Num_up["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    Control_reset_H = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": "Control_reset_H"},"BlockObject": {"Coordinates": {"X": 0,"Y": 2,"Z": 0}},"Relay": {"Mode": "Or","InputA": Num_left["Id"],"InputB": Num_right["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    Control_reset_up = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": "Control_reset_up"},"BlockObject": {"Coordinates": {"X": 5,"Y": 4,"Z": 0}},"Relay": {"Mode": "Or","InputA": Control_reset_H["Id"],"InputB": Num_down["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    Control_reset_down = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": "Control_reset_down"},"BlockObject": {"Coordinates": {"X": 3,"Y": 2,"Z": 0}},"Relay": {"Mode": "Or","InputA": Control_reset_H["Id"],"InputB": Num_up["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    Control_reset_right = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": "Control_reset_right"},"BlockObject": {"Coordinates": {"X": 5,"Y": 2,"Z": 0}},"Relay": {"Mode": "Or","InputA": Control_reset_V["Id"],"InputB": Num_left["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    Control_reset_left = {"Id": str(uuid.uuid4()),"Template": "Relay.IronTeeth","Components": {"NamedEntity": {"EntityName": "Control_reset_left"},"BlockObject": {"Coordinates": {"X": 3,"Y": 4,"Z": 0}},"Relay": {"Mode": "Or","InputA": Control_reset_V["Id"],"InputB": Num_right["Id"]},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 1}]}}}}
    entities.append(Control_reset_V)
    entities.append(Control_reset_H)
    entities.append(Control_reset_up)
    entities.append(Control_reset_down)
    entities.append(Control_reset_right)
    entities.append(Control_reset_left)
    State_up = generate_memory(4, 4, 0, "State_up", Num_up["Id"], Control_reset_up["Id"])
    State_down = generate_memory(4, 2, 0, "State_down", Num_down["Id"], Control_reset_down["Id"])
    State_left = generate_memory(3, 3, 0, "State_left", Num_right["Id"], Control_reset_right["Id"])
    State_right = generate_memory(5, 3, 0, "State_right", Num_left["Id"], Control_reset_left["Id"])
    entities.append(State_up)
    entities.append(State_down)
    entities.append(State_right)
    entities.append(State_left)
    entities.append(generate_lamp(4, 0, 0, State_down["Id"]))
    entities.append(generate_lamp(3, 1, 0, State_down["Id"]))
    entities.append(generate_lamp(4, 1, 0, State_down["Id"]))
    entities.append(generate_lamp(5, 1, 0, State_down["Id"]))
    entities.append(generate_lamp(3, 5, 0, State_up["Id"]))
    entities.append(generate_lamp(4, 5, 0, State_up["Id"]))
    entities.append(generate_lamp(5, 5, 0, State_up["Id"]))
    entities.append(generate_lamp(4, 6, 0, State_up["Id"]))
    entities.append(generate_lamp(2, 2, 0, State_left["Id"]))
    entities.append(generate_lamp(2, 3, 0, State_left["Id"]))
    entities.append(generate_lamp(2, 4, 0, State_left["Id"]))
    entities.append(generate_lamp(1, 3, 0, State_left["Id"]))
    entities.append(generate_lamp(6, 2, 0, State_right["Id"]))
    entities.append(generate_lamp(6, 3, 0, State_right["Id"]))
    entities.append(generate_lamp(6, 4, 0, State_right["Id"]))
    entities.append(generate_lamp(7, 3, 0, State_right["Id"]))
    food_flag = {"Id": str(uuid.uuid4()),"Template": "PowerMeter.IronTeeth","Components": {"NamedEntity": {"EntityName": "food_flag"},"BlockObject": {"Coordinates": {"X": 8,"Y": 0,"Z": 0},"Orientation": "Cw270"},"PowerMeter": {"Mode": "BatteryChargeLevel","ComparisonMode": "Greater","IntThreshold": 0,"PercentThreshold": 0.5},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Gear","Amount": 10},{"Good": "MetalBlock","Amount": 6}]}}}}
    entities.append(food_flag)
    entities.append({"Id": str(uuid.uuid4()),"Template": "GravityBattery.IronTeeth","Components": {"BlockObject": {"Coordinates": {"X": 9,"Y": 1,"Z": 0},"Orientation": "Cw270"},"LayeredVerticalBlockObstacle": {"OccupancyRange": 0.0},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 40},{"Good": "Gear","Amount": 40},{"Good": "MetalBlock","Amount": 10}]}}}})

cell_table = [[{} for _ in range(grid_y)] for _ in range(grid_x)]

def create_cell(px, py):
    cell = []
    x = offfset_x + (2 * px)
    y = offfset_y + (2 * py)
    place_tower(x, y)
    place_tower(x, y + 1)
    place_tower(x + 1, y)
    place_tower(x + 1, y + 1)
    isBody = generate_memory(x, y, 0, str(px) + "_" + str(py) + "_isBody", temp["Id"], temp["Id"])
    isHead = generate_memory(x + 1, y, 0, str(px) + "_" + str(py) + "_isHead", temp["Id"], temp["Id"])
    isFood = generate_memory(x, y + 1, 0, str(px) + "_" + str(py) + "_isFood", temp["Id"], temp["Id"])
                
    in_body_OR_1_1 = generate_relay(x, y, 2, "in_body_OR_1_1", "Or", temp["Id"], temp["Id"])
    in_body_OR_1_2 = generate_relay(x + 1, y, 2, "in_body_OR_1_2", "Or", temp["Id"], temp["Id"])
    in_body_AND_1_1 = generate_relay(x, y + 1, 2, "in_body_AND_1_1", "And", temp["Id"], temp["Id"])
    in_body_AND_1_2 = generate_relay(x + 1, y + 1, 2, "in_body_AND_1_2", "And", temp["Id"], temp["Id"])
    in_body_OR_2_1 = generate_relay(x, y, 4, "in_body_OR_2_1", "Or", in_body_OR_1_1["Id"], in_body_OR_1_2["Id"])
    in_body_OR_2_2 = generate_relay(x + 1, y, 4, "in_body_OR_2_2", "Or", in_body_AND_1_1["Id"], in_body_AND_1_2["Id"])
    in_body_AND_2_1 = generate_relay(x, y + 1, 4, "in_body_AND_2_1", "And", in_body_OR_1_1["Id"], in_body_OR_1_2["Id"])
    in_body_AND_2_2 = generate_relay(x + 1, y + 1, 4, "in_body_AND_2_2", "And", in_body_AND_1_1["Id"], in_body_AND_1_2["Id"])
    in_body_AND_3_1 = generate_relay(x, y, 6, "in_body_AND_3_1", "And", in_body_OR_2_1["Id"], in_body_AND_2_2["Id"])
    in_body_OR_3_1 = generate_relay(x + 1, y, 6, "in_body_OR_3_1", "Or", in_body_OR_2_1["Id"], in_body_AND_2_2["Id"])
    in_body_NOT_1 = generate_denial(x, y + 1, 6, "in_body_NOT_1", in_body_AND_3_1["Id"])
    in_body_Exactly_two = generate_relay(x, y, 8, "in_body_Exactly_two", "And", in_body_NOT_1["Id"], in_body_OR_3_1["Id"])
    in_body_NOT_2 = generate_denial(x + 1, y + 1, 6, "in_body_NOT_2", in_body_OR_3_1["Id"])
    in_body_Exactly_one = generate_relay(x + 1, y, 8, "in_body_Exactly_one", "And", in_body_NOT_2["Id"], in_body_OR_2_2["Id"])#  not sure if ^ this ^ needs or_2_2 or or_2_1
    stay_body_1 = generate_relay(x, y + 1, 8, "stay_body_1", "And", in_body_Exactly_two["Id"], isBody["Id"])
    stay_body = generate_relay(x + 1, y, 10, "stay_body", "Or", stay_body_1["Id"], isHead["Id"])
    grow_tail = generate_relay(x + 1, y + 1, 8, "grow_tail", "Or", food_flag["Id"], in_body_Exactly_one["Id"])
    Calculated_body_input = generate_relay(x, y, 10, "body_input", "Or", stay_body["Id"], grow_tail["Id"])
    manual_body_input =  {"Id": str(uuid.uuid4()),"Template": "Lever.IronTeeth","Components": {"NamedEntity": {"EntityName": str(px) + "_" + str(py) + "manual_body_input"},"BlockObject": {"Coordinates": {"X": x + 1,"Y": y,"Z": 30},"Orientation": "Cw270"},"Lever": {"IsSpringReturn": false,"IsPinned": false},"Automator": {"State": "Off"},"Inventory:ConstructionSite": {"Storage": {"Goods": [{"Good": "Plank","Amount": 1},{"Good": "Gear","Amount": 2}]}}}}
    body_input = generate_relay(x, y + 1, 10, "body_input", "Or", Calculated_body_input["Id"], manual_body_input["Id"])
    body_tick = generate_relay(x + 1, y + 1, 10, "body_tick", "And", body_input["Id"], clock["Id"])
    body_oppose = generate_denial(x, y, 12, "body_oppose", body_tick["Id"])
    set_Set(isBody, body_tick["Id"])
    set_Reset(isBody, body_oppose["Id"])

    cell.append(isBody)
    cell.append(isHead)
    cell.append(isFood)
    entities.append(generate_lamp(x, y, 32, isBody["Id"]))
    entities.append(generate_lamp(x + 1, y, 32, isBody["Id"]))
    entities.append(generate_lamp(x, y + 1, 32, isBody["Id"]))
    entities.append(generate_lamp(x + 1, y + 1, 32, isBody["Id"]))
    cell.append(in_body_OR_1_1)
    cell.append(in_body_OR_1_2)
    cell.append(in_body_AND_1_1)
    cell.append(in_body_AND_1_2)
    cell.append(in_body_OR_2_1)
    cell.append(in_body_OR_2_2)
    cell.append(in_body_AND_2_1)
    cell.append(in_body_AND_2_2)
    cell.append(in_body_AND_3_1)
    cell.append(in_body_OR_3_1)
    cell.append(in_body_NOT_1)
    cell.append(in_body_Exactly_two)
    cell.append(in_body_NOT_2)
    cell.append(in_body_Exactly_one)
    cell.append(stay_body_1)
    cell.append(stay_body)
    cell.append(grow_tail)
    cell.append(Calculated_body_input)
    cell.append(manual_body_input)
    cell.append(body_input)
    cell.append(body_tick)
    cell.append(body_oppose)

    for _ in cell:
        entities.append(_)

    cell_table[px - 5][py - 5] = cell


def connect_logic():
    for px in range(grid_x):
        for py in range(grid_y):
            x = px
            y = py
            cell = cell_table[x % grid_x][y % grid_x]
            east = cell_table[(x + 1) % grid_x][y]
            west = cell_table[(x - 1) % grid_x][y]
            north = cell_table[x][(y + 1) % grid_y]
            south = cell_table[x][(y - 1) % grid_y]
            e = get_by_name(east, str((x + 1) % grid_x) + "_" + str(y) + "_isBody")
            if (e == None):
                continue
            c = get_by_name(cell, "in_body_OR_1_1")
            set_InputA(c, e["Id"])
            c = get_by_name(cell, "in_body_AND_1_1")
            set_InputA(c, e["Id"])

            e = get_by_name(west, str((x - 1) % grid_x) + "_" + str(y) + "_isBody")
            if (e == None):
                continue
            c = get_by_name(cell, "in_body_OR_1_1")
            set_InputB(c, e["Id"])
            c = get_by_name(cell, "in_body_AND_1_1")
            set_InputB(c, e["Id"])

            e = get_by_name(north, str(x) + "_" + str((y + 1) % grid_y) + "_isBody")
            if (e == None):
                continue
            c = get_by_name(cell, "in_body_OR_1_2")
            set_InputA(c, e["Id"])
            c = get_by_name(cell, "in_body_AND_1_2")
            set_InputA(c, e["Id"])

            e = get_by_name(south, str(x) + "_" + str((y - 1) % grid_y) + "_isBody")
            if (e == None):
                continue
            c = get_by_name(cell, "in_body_OR_1_2")
            set_InputB(c, e["Id"])
            c = get_by_name(cell, "in_body_AND_1_2")
            set_InputB(c, e["Id"])

create_controls()

for x in range(grid_x):
    for y in range(grid_y):
        create_cell(x, y)

connect_logic()

world_x =  world["Singletons"]["MapSize"]["Size"]["X"]
world_y =  world["Singletons"]["MapSize"]["Size"]["Y"]

out = open("saves/world.json", "w")
json.dump(world, out)
