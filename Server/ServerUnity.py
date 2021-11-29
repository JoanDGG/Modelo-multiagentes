# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. October 2021

from flask import Flask, request, jsonify
from Agents import *
from Model import TrafficModel

# Default elements of the model:

number_agents = 10
current_step = 0
# max_steps = 100

app = Flask("Traffic Model")

# @app.route('/', methods=['POST', 'GET'])

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global traffic_model, number_agents, current_step

    if request.method == 'POST':
        number_agents = int(request.form.get('NAgents'))
        current_step = 0
        #max_steps = int(request.form.get('maxSteps'))
        traffic_model = TrafficModel(number_agents)
        return jsonify({"message":"Parameters recieved, model initiated."})

    #elif request.method == 'GET':
    #    return jsonify({'drop_zone_pos': [{"x": warehouse_model.drop_zone[0], "y": warehouse_model.drop_zone[1]}]})

@app.route('/getRobotAgents', methods=['GET'])
def getAgents():
    global traffic_model

    if request.method == 'GET':
        robots_attributes = sorted([{"x": x, "y": 1, "z": z, "has_box": a.has_box, "unique_id": a.unique_id} for (a, x, z) in traffic_model.grid.coord_iter() if isinstance(a, Car)], key=lambda item: item["unique_id"])
#        for robot_attributes in robots_attributes:
#            print(robot_attributes)
        return jsonify({'robots_attributes': robots_attributes})

@app.route('/getTraffic_Lights', methods=['GET'])
def getTraffic_Lights():
    global traffic_model

    if request.method == 'GET':
        traffic_lightPositions = sorted([{"x": x, "y":1, "z":z, "unique_id": a.unique_id}  for (a, x, z) in traffic_model.grid.coord_iter() if isinstance(a, Traffic_Light)], key=lambda item: item["unique_id"])
        return jsonify({'obstacles_attributes':traffic_lightPositions})

@app.route('/getDestinations', methods=['GET'])
def getDestinations():
    global traffic_model

    if request.method == 'GET':
        destinationPositions = sorted([{"x": x, "y":1, "z":z, "unique_id": a.unique_id}  for (a, x, z) in traffic_model.grid.coord_iter() if isinstance(a, Destination)], key=lambda item: item["unique_id"])
        return jsonify({'obstacles_attributes':destinationPositions})

@app.route('/getObstacles', methods=['GET'])
def getObstacles():
    global traffic_model

    if request.method == 'GET':
        obstaclePositions = sorted([{"x": x, "y":1, "z":z, "unique_id": a.unique_id}  for (a, x, z) in traffic_model.grid.coord_iter() if isinstance(a, Obstacle)], key=lambda item: item["unique_id"])
        return jsonify({'obstacles_attributes':obstaclePositions})

@app.route('/getRoads', methods=['GET'])
def getRoads():
    global traffic_model

    if request.method == 'GET':
        roadPositions = sorted([{"x": x, "y":1, "z":z, "unique_id": a.unique_id}  for (a, x, z) in traffic_model.grid.coord_iter() if isinstance(a, Road)], key=lambda item: item["unique_id"])
        return jsonify({'obstacles_attributes':roadPositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global current_step, traffic_model
    if request.method == 'GET':
        traffic_model.step()
        current_step += 1
        return jsonify({'currentStep':current_step})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)