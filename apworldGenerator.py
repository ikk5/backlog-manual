import os
import shutil
from pathlib import Path

# constants
players_path = r"players/"
output_path = r"output/"
json_path = r"json templates/"
game_json = "game.json"
items_json = "items.json"
locations_json = "locations.json"
yaml = "Manual_Backlog_.yaml"

# methods
def clearOutput():
    for file in os.listdir(output_path):
        if os.path.isdir(output_path+file):
            shutil.rmtree(output_path+file)
        else:
            os.remove(output_path + file)

def replacePlaceholder(placeholder, replacement, filepath):
    with open(filepath, 'r') as file:
        filedata = file.read()
    filedata = filedata.replace(placeholder, replacement)

    with open(filepath, 'w') as file:
        file.write(filedata)
    file.close()

def createInitialOutput(player_name, player_output):
    shutil.copytree("empty apworld", player_output)

    yaml_output = output_path + yaml.split(".")[0] + player_name + ".yaml"
    shutil.copy(json_path + yaml, yaml_output)
    replacePlaceholder("<PLAYER>", player_name, yaml_output)

    game_output = player_output + r"/data/"+game_json
    shutil.copy(json_path+game_json, game_output)
    replacePlaceholder("<PLAYER>", player_name, game_output)

    shutil.copy(json_path+items_json, player_output + r"/data/"+items_json)
    shutil.copy(json_path+locations_json, player_output + r"/data/"+locations_json)

def insertJsonLine(line_to_insert, file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        insert_position = len(lines) -2
        lines.insert(insert_position, line_to_insert)
    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line)
    file.close()

def addGameToItems(title, player_output):
    item = ',{"name": "'+title+' pass", "category": ["Game"], "progression": true}\n'
    insertJsonLine(item, player_output + r"/data/"+items_json)

def addGameToLocations(title, player_output):
    locations = (',{"name": "'+title+' beaten reward 1", "category": ["'+title+'"], "requires": "|'+title+' pass|"}\n'
                 ',{"name": "'+title+' beaten reward 2", "category": ["'+title+'"], "requires": "|'+title+' pass|"}\n')
    insertJsonLine(locations, player_output + r"/data/"+locations_json)

def buildApworld(player_name):
    output_file = output_path+"manual_backlog_"+player_name
    # zip folder
    shutil.make_archive(output_file, "zip", output_file)
    # change zip extension to apworld
    file = Path(output_file + ".zip")
    new_file = file.with_suffix(".apworld")
    file.rename(new_file)
    # cleanup zipped folders
    shutil.rmtree(output_file)

#actual script start
clearOutput()
player_list = os.listdir(players_path)
for playertxt in player_list:
    if not playertxt.startswith("template"):
        player_name = playertxt.split(".")[0].strip()
        player_output = output_path + r"manual_backlog_" + player_name + "/" + player_name
        createInitialOutput(player_name, player_output)

        with open(players_path + playertxt) as file:
            required_goal_items = file.readline().split("=")[1].strip()
            replacePlaceholder("<GOAL_ITEMS_REQUIRED>", required_goal_items, player_output + r"/data/"+locations_json)
            available_goal_items = file.readline().split("=")[1].strip()
            replacePlaceholder("<GOAL_ITEMS_AVAILABLE>", available_goal_items, player_output + r"/data/"+items_json)

            for line in file:
                if not line.startswith("#") and not line.isspace():
                    line = line.strip().replace(":", "")
                    addGameToItems(line, player_output)
                    addGameToLocations(line, player_output)
        file.close()
        buildApworld(player_name)

