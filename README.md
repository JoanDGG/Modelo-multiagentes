# Multi agent model

Project in Unity/Flask to model a multi agent behaviour for a car simulation

# Unity simulation
## Instructions to run Unity simulation

- Open the 'Executables' folder
- Download the zip file for the map you want to open (depending on wether you have Windows or MacOS):

```
  - Modelo multiagentes_Mapa grande
  - Modelo multiagentes_Mapa original
  - Modelo multiagentes_Mapa pequeño
```

- Export and execute the program 'Modelo multiagentes.exe'

# Python web server simulation
## Setup instructions

- Strongly recommend using a custom conda environment.
- Install python 3.8 in the environment: ```conda install python=3.8``` Using 3.8 for compatibility reasons. Maybe 3.9 or 3.10 are compatible with all the packages, but will have to check.
- Installing mesa: ```pip install mesa```
- Installing flask to mount the service: ```pip install flask```

## Instructions to run Python web server simulation


- You can run the python web server display by executing the program ```Server/ServerWeb.py```. This will open a new window at your default browser with the simulation.
- To run the python web server, you can use the following command:

```
python ServerWeb.py
```

- To choose the map you want to simulate, you will have to change the txt file of the choosen map to 'base.txt', make sure non other has the same name.

# Develompent team:

- Daniel García Barajas       A01378688
- Joan Daniel Guerrero García A01378052
- Luis Ignacio Ferro Salinas  A01378248

## Disclaimers
It seems that for the simulation of the map with 60 destinations doesn't boot up correctly a very small percentage of the times that it is run. If this happens, try re-openning it a few times, that should be enough to make it work.

### Reading the map
* If testing a map, running the server locally, the turns of the map should be just like the ones in the original base.txt map. 
* Don't place destinations in the intersections where there are traffic lights.
* Don't substitute traffic lights with destinations.