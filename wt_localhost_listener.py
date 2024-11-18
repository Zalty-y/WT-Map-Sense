import aiohttp
import asyncio
import time
import json
import os
import math

# URL for War Thunder's localhost server
player_movement_url = "http://localhost:8111/map_obj.json"
match_status_url = "http://localhost:8111/map_info.json"
map_info_url = "http://localhost:8111/map_info.json"

previous_data = None
map_info = None
match_active = None
def_listen_interval = 250
match_start_time = None

blue = "#185AFF"
red = "#fa3200"
team_one = ""
team_two = ""

async def check_for_update(session):
    global match_active

    async with session.get(match_status_url) as response:
        map_info = await response.json()
        match_active = map_info["valid"]
    
    if not match_active:
        return None

    async with session.get(player_movement_url) as response:
        data = await response.json()
        return data

async def event_listener():
    global previous_data
    global match_start_time
    global map_info
    previous_update_time_ms = time.time()
    current_update_time_ms = 0
    total = 0
    averageCount = 0
    listen_interval_ms = def_listen_interval
    match_end_time = None
    logged_map_obj_data = {}

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                # Fetch data and compare with previous data
                current_data = await check_for_update(session)

                if match_active and not match_start_time: #current_data and previous_data is None:
                    print("Match started!")

                    async with session.get(map_info_url) as response:
                        map_info = await response.json()

                    total = 0
                    averageCount = 0
                    listen_interval_ms = def_listen_interval
                    match_start_time = time.time()
                    match_end_time = None
                    logged_map_obj_data = {}
                elif not match_active and match_start_time: #previous_data and current_data is None:
                    print("Match ended!")
                    match_start_time = None
                    match_end_time = time.time()

                    # Save the dictionary as JSON
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    file_path = os.path.join(script_dir, "TODO_MATCH_ID_" + str(int(time.time())) + ".json")
                    with open(file_path, "w") as file:
                        json.dump(logged_map_obj_data, file, indent=4)

                if match_start_time and previous_data and current_data != previous_data:
                    current_update_time_ms = time.time()
                    update_time_diff_ms = int((current_update_time_ms - previous_update_time_ms) * 1000)
                    
                    if update_time_diff_ms > 200 and update_time_diff_ms < 350:

                        # listening interval is the shortest time between updates on port 8111
                        listen_interval_ms = min(listen_interval_ms, update_time_diff_ms)

                        total += update_time_diff_ms
                        averageCount += 1
                        print("Average:\t" + str(int(total / averageCount)) + "ms")
                        print("Minimum:\t" + str(listen_interval_ms))

                    previous_update_time_ms = current_update_time_ms
                    # Place your event-handling code here
                    # e.g., process or log the updated data

                    # print(current_data)
                    await append_data(logged_map_obj_data, current_data)
                    print(len(logged_map_obj_data))

                # Update previous_data for the next loop
                previous_data = current_data
                
                # Small delay to avoid overwhelming the server
                # Set delay to rollingAvg - 30ms
                await asyncio.sleep(listen_interval_ms / 1000)
                # - int(current_update_time_ms - time.time()))  # Adjust delay as needed

            except Exception as e:
                print(f"Error occurred: {e}\nMake sure the game is running before launching this program.")
                break

async def append_data(data, new_data):
    if not match_start_time:
        raise Exception("Match has not started!")
    data[round(time.time() - match_start_time, 2)] = new_data

def get_spawns(data):
    global team_one
    global team_two

    spawns = {
        "air": [
            {
                "team": 1,
                "spawns": []
            },
            {
                "team": 2,
                "spawns": []
            },
            {
                "team": 0,
                "spawns": []
            }
        ],
        "ground": [
            {
                "team": 1,
                "spawns": []
            },
            {
                "team": 2,
                "spawns": []
            },
            {
                "team": 0,
                "spawns": []
            }
        ]
    }

    air_blue = []
    air_red = []
    air_neut = []

    ground_blue = []
    ground_red = []
    ground_neut = []

    for spawn in data:
        if spawn["type"] == "airfield":
            if spawn["color"] is blue:
                air_blue.append(spawn)
            elif spawn["color"] is red:
                air_red.append(spawn)
            else:
                air_neut.append(spawn)
        elif spawn["type"] == "respawn_base_tank":
            if spawn["color"] is blue:
                ground_blue.append(spawn)
            elif spawn["color"] is red:
                ground_red.append(spawn)
            else:
                ground_neut.append(spawn)
        else:
            continue

    # Assign team numbers based on spawn location on map.
    avg_ground_blue = (sum([spawn["x"] for spawn in ground_blue]) / len(ground_blue),
                      sum([spawn["y"] for spawn in ground_blue]) / len(ground_blue))
    
    map_size = map_info["map_max"]

    # The spawns below a line pulled from the top left of the map to the
    # bottom right will be classified as team one.
    if (avg_ground_blue[1] <= avg_ground_blue[0]):
        team_one = blue
        team_two = red
        air_team_one = air_blue
        air_team_two = air_red
        ground_team_one = ground_blue
        ground_team_two = ground_red
    else:
        team_one = red
        team_two = blue
        air_team_one = air_red
        air_team_two = air_blue
        ground_team_one = ground_red
        ground_team_two = ground_blue

    for air_spawn in spawns["air"]:
        if air_spawn["team"] == 1:
            air_spawn["spawns"] = air_team_one
        elif air_spawn["team"] == 2:
            air_spawn["spawns"] = air_team_two
        else:
            air_spawn["spawns"] = air_neut

    for ground_spawn in spawns["ground"]:
        if ground_spawn["team"] == 1:
            ground_spawn["spawns"] = ground_team_one
        elif ground_spawn["team"] == 2:
            ground_spawn["spawns"] = ground_team_two
        else:
            ground_spawn["spawns"] = ground_neut
        
    # Save the dictionary as JSON
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "TODO_MATCH_ID_SPAWNS_" + str(int(time.time())) + ".json")
    with open(file_path, "w") as file:
        json.dump(spawns, file, indent=4) 

def vector_angle(a, b):
    return math.acos((a[0] * b[0] + a[1] * b[1]) /
                     (math.sqrt(pow(a[0], 2) + pow(a[1], 2)) *
                      math.sqrt(pow(b[0], 2) + pow(b[1], 2))))

# Run the asynchronous event listener
asyncio.run(event_listener())
