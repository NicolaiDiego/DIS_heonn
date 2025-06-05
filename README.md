We chose to pivot into a Pokemon Gen 3 Wiki/"Cheat Sheet" since it made more sense for us. We found a great dataset and ran with it.

# Pokemon Gen 3 Trainer Guide
This web app helps players with trainer battles in Pokémon Ruby, Sapphire, Emerald, and their remakes.

Pick a route to see all trainers in that area.
Select a trainer to check their Pokémon, moves, and rewards.
See how much money and EXP you get for winning.

If you know a trainer’s name, you can search for them directly in the search bar.

### Requirements

Have Docker installed on your system. 
https://www.docker.com/products/docker-desktop/

Have Postgresql installed.
https://www.postgresql.org/download/


### How To Run
Clone or Download repository files: https://github.com/NicolaiDiego/DIS_heonn/archive/refs/heads/main.zip

The database and web-app is then run by in ur terminal:

	docker compose up --build

*Ensure the path is set to the working directory*

The web-app can then be found at:

	http://127.0.0.1:5000
