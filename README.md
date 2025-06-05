# Pokemon Gen 3 wiki
This webapp is designed with the intention of helping players defeat all trainers in the 3rd generation of pokemon games. You simply find the route you're at, and select the trainer you want to know more about. The webapp will then show you what pokemon the trainer has, what moves the pokemon has and how much money/exp you get from defeating said trainer. If you know the name of a trainer you can simply search up the name and instantly find the trainer without having to look through all the routes.z


###

Have Docker installed on your system. 
https://www.docker.com/products/docker-desktop/

Have Postgresql installed.
https://www.postgresql.org/download/


###
Clone or Download repository files: https://github.com/NicolaiDiego/DIS_heonn/archive/refs/heads/main.zip

The database and web-app is then run by:

	docker compose up --build

The web-app can then be found at 

	http://127.0.0.1:5000
