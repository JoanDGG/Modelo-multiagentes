# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. October 2021

from flask import Flask, request, jsonify
from Agents import *
from Model import TrafficModel

# Default elements of the model:

# number_agents = 10
traffic_model = None
current_step = 0
# max_steps = 100

app = Flask("Traffic Model")

# @app.route('/', methods=['POST', 'GET'])

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global traffic_model, current_step

    if request.method == 'GET': # POST
        # number_agents = int(request.form.get('NAgents'))
        current_step = 0
        #max_steps = int(request.form.get('maxSteps'))
        traffic_model = TrafficModel()
        # print("Model at init: ", traffic_model)
        return jsonify({"width":traffic_model.width, "height": traffic_model.height})

    #elif request.method == 'GET':
    #    return jsonify({'drop_zone_pos': [{"x": warehouse_model.drop_zone[0], "y": warehouse_model.drop_zone[1]}]})

@app.route('/getCarAgents', methods=['GET'])
def getAgents():
    global traffic_model

    if request.method == 'GET':
        cars_attributes = sorted([{"x": x, "y": 0.35, "z": z, "unique_id": b.unique_id} for (a, x, z) in traffic_model.grid.coord_iter() for b in a if isinstance(b, Car)], key=lambda item: item["unique_id"])
        # print("Model at getCarAgents: ", traffic_model)
        # for car_attributes in cars_attributes:
        #     print(car_attributes)
        return jsonify({'cars_attributes': cars_attributes})

@app.route('/getTraffic_Lights', methods=['GET'])
def getTraffic_Lights():
    global traffic_model

    if request.method == 'GET':
        traffic_light_attributes = sorted([{"x": x, "y":1.01, "z":z, "state": b.state, "unique_id": b.unique_id}  for (a, x, z) in traffic_model.grid.coord_iter() for b in a if isinstance(b, Traffic_Light)], key=lambda item: item["unique_id"])
        return jsonify({'traffic_light_attributes':traffic_light_attributes})

@app.route('/getDestinations', methods=['GET'])
def getDestinations():
    global traffic_model

    if request.method == 'GET':
        destination_positions = sorted([{"x": x, "y":0.01, "z":z, "unique_id": b.unique_id}  for (a, x, z) in traffic_model.grid.coord_iter() for b in a if isinstance(b, Destination)], key=lambda item: item["unique_id"])
        return jsonify({'destination_positions':destination_positions})

@app.route('/getObstacles', methods=['GET'])
def getObstacles():
    global traffic_model

    if request.method == 'GET':
        obstacle_positions = sorted([{"x": x, "y":1, "z":z, "unique_id": b.unique_id}  for (a, x, z) in traffic_model.grid.coord_iter() for b in a if isinstance(b, Obstacle)], key=lambda item: item["unique_id"])
        print("Obstacles-> ",len(obstacle_positions))
        return jsonify({'obstacles_attributes':obstacle_positions})

@app.route('/getRoads', methods=['GET'])
def getRoads():
    global traffic_model

    if request.method == 'GET':
        road_attributes = sorted([{"x": x, "y":0.01, "z":z, "directions": b.direction, "unique_id": b.unique_id}  for (a, x, z) in traffic_model.grid.coord_iter() for b in a if isinstance(b, Road)], key=lambda item: item["unique_id"])
        return jsonify({'road_attributes':road_attributes})

@app.route('/update', methods=['GET'])
def updateModel():
    global current_step, traffic_model
    if request.method == 'GET':
        traffic_model.step()
        current_step += 1
        return jsonify({'currentStep':current_step})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)