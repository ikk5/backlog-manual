# backlog-manual

This script will generate an apworld and yaml for every player, using the games you listed as items and locations.

Steps to generate an apworld for your backlog:
1. In the players folder, duplicate the template.txt for every player and rename them with the playernames
2. List the games for every player in their txt file, make sure every game is on a new line
3. In the same txt file, add the number of required and available goal items
    I've only tested it with 10 games, 3 required and 4 available goal items and that requires every player to beat around 4 games.
4. Make sure you have nothing in the output folder you don't mind losing, cause this script will clear that folder before generating the new apworlds and yamls
5. Run apworldGenerator (.py or .exe)
6. Install all the generated apworlds in the output folder or move them to the custom worlds folder
7. Move the generated yamls from the output folder to your Archipelago/Players folder
8. Generate and host the game as you're used to