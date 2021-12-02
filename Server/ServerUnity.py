# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz and Octavio Navarro.
# Last modified 2 December 2021

from flask import Flask, request, jsonify
from Agents import *
from Model import TrafficModel

# Default elements of the model:
traffic_model = None
current_step = 0

app = Flask("Traffic Model")

# @app.route('/', methods=['POST', 'GET'])

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global traffic_model, current_step

    if request.method == 'GET':
        current_step = 0
        traffic_model = TrafficModel()
        return jsonify({"width":traffic_model.width, "height": traffic_model.height})

@app.route('/getCarAgents', methods=['GET'])
def getAgents():
    global traffic_model

    if request.method == 'GET':
        cars_attributes = sorted([{"x": x, "y": 0.35, "z": z, "unique_id": b.unique_id, "arrived": b.arrived} for (a, x, z) in traffic_model.grid.coord_iter() for b in a if isinstance(b, Car)], key=lambda item: item["unique_id"])
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
        return jsonify({'obstacles_attributes':obstacle_positions})

@app.route('/getRoads', methods=['GET'])
def getRoads():
    global traffic_model

    if request.method == 'GET':
        road_attributes = sorted([{"x": x, "y":0.01, "z":z, "directions": b.directions, "unique_id": b.unique_id}  for (a, x, z) in traffic_model.grid.coord_iter() for b in a if isinstance(b, Road)], key=lambda item: item["unique_id"])
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