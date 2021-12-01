// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. October 2021

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

[System.Serializable]
public class CarData
{
    public float x, y, z;
    public int unique_id;
}

[System.Serializable]
public class TrafficLightData
{
    public float x, y, z;
    public bool state;
    public string unique_id;
}

[System.Serializable]
public class DestinationData
{
    public float x, y, z;
    public string unique_id;
}

[System.Serializable]
public class ObstacleData
{
    public float x, y, z;
    public string unique_id;
}

[System.Serializable]
public class RoadData
{
    public float x, y, z;
    public string direction;
    public string unique_id;
}


[System.Serializable]
public class CarsData
{
    public List<CarData> cars_attributes;
}

[System.Serializable]
public class TrafficLightsData
{
    public List<TrafficLightData> traffic_light_attributes;
}

[System.Serializable]
public class DestinationsData
{
    public List<DestinationData> destination_positions;
}

[System.Serializable]
public class ObstaclesData
{
    public List<ObstacleData> obstacle_positions;
}

[System.Serializable]
public class RoadsData
{
    public List<RoadData> road_attributes;
}

[System.Serializable]
public class GridData
{
    public int width;
    public int height;
}
[System.Serializable]
public class ModelData
{
    public int currentStep;
}

public class AgentController : MonoBehaviour
{
    // private string url = "https://boids.us-south.cf.appdomain.cloud/";
    string serverUrl = "http://localhost:8585";
    string sendConfigEndpoint = "/init";
    string getCarsEndpoint = "/getCarAgents";
    string getTrafficLigtsEndpoint = "/getTraffic_Lights";
    string getDestinationsEndpoint = "/getDestinations";
    string getObstaclesEndpoint = "/getObstacles";
    string getRoadsEndpoint = "/getRoads";
    string updateEndpoint = "/update";
    CarsData carsData;
    TrafficLightsData trafficLightsData;
    DestinationsData destinationsData;
    ObstaclesData obstacleData;
    RoadsData roadsData;
    GameObject[] carsGameObjects;
    List<Vector3> oldPositions;
    List<Vector3> newPositions;
    bool hold = false;

    public GameObject[] carPrefabs = new GameObject[5];
    public GameObject trafficLightPrefab, destinationPrefab, buildingPrefab, roadPrefab, reloadButton;
    public Text currentStep;
    //public int NAgents, NBoxes, width, height, maxShelves, maxSteps;
    public float timeToUpdate = 0.5f, timer, dt;

    void Start()
    {
        carsData = new CarsData();
        trafficLightsData = new TrafficLightsData();
        destinationsData = new DestinationsData();
        obstacleData = new ObstaclesData();
        roadsData = new RoadsData();
        oldPositions = new List<Vector3>();
        newPositions = new List<Vector3>();

        //floor.transform.localScale = new Vector3((float)width/10, 1, (float)height/10);
        //floor.transform.localPosition = new Vector3((float)width/2-0.5f, 0, (float)height/2-0.5f);
        
        timer = timeToUpdate;

        InitialConfiguration();
    }

    private void Update() 
    {
        float t = timer/timeToUpdate;
        // Smooth out the transition at start and end
        dt = t * t * ( 3f - 2f*t);

        if(timer >= timeToUpdate)
        {
            timer = 0;
            hold = true;
            StartCoroutine(UpdateSimulation());
        }

        if (!hold)
        {
            for (int s = 0; s < carsGameObjects.Length; s++)
            {
                Vector3 interpolated = Vector3.Lerp(oldPositions[s], newPositions[s], dt);
                carsGameObjects[s].transform.localPosition = interpolated;
                
                Vector3 dir = oldPositions[s] - newPositions[s];
                if(dir != new Vector3(0, 0, 0))
                    carsGameObjects[s].transform.rotation = Quaternion.LookRotation(dir);
                
            }
            // Move time from the last frame
            timer += Time.deltaTime;
        }
    }
 
    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            ModelData model = JsonUtility.FromJson<ModelData>(www.downloadHandler.text);
            currentStep.text = "Step " + model.currentStep;
            /*
            if(model.currentStep >= maxSteps)
            {
                currentStep.text += "\nSimulation complete.";
                reloadButton.SetActive(true);
            }
            else
            {
                StartCoroutine(UpdateRobotsData());
                StartCoroutine(UpdateObstaclesData());
            }
            */
            StartCoroutine(UpdateCarsData());
            StartCoroutine(UpdateWorldData());
        }
    }

    public void InitialConfiguration()
    {
        GameObject[] cars = GameObject.FindGameObjectsWithTag("Car");
        foreach(GameObject car in cars)
            GameObject.Destroy(car);
        StartCoroutine(SendConfiguration());
    }
    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();
        /*
        form.AddField("NAgents", NAgents.ToString());
        form.AddField("NBoxes", NBoxes.ToString());
        form.AddField("width", width.ToString());
        form.AddField("height", height.ToString());
        form.AddField("maxShelves", maxShelves.ToString());
        form.AddField("maxSteps", maxSteps.ToString());
        */
        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            //Debug.Log("Configuration upload complete!");
            StartCoroutine(GetCarsData());
            StartCoroutine(GetWorldData());
        }
        /*
        www = UnityWebRequest.Get(serverUrl + sendConfigEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            // Assign position to the drop zone
            Drop_zones drop_zones = JsonUtility.FromJson<Drop_zones>(www.downloadHandler.text);
            drop_zone.transform.position = new Vector3(drop_zones.drop_zone_pos[0].x,
                                                       drop_zone.transform.position.y, 
                                                       drop_zones.drop_zone_pos[0].y);
        }
        */
    }

    IEnumerator GetCarsData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getCarsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            carsData = JsonUtility.FromJson<CarsData>(www.downloadHandler.text);
            carsGameObjects = new GameObject[carsData.cars_attributes.Count];

            // Store the old positions for each agent
            for (int index_car = 0; index_car < carsData.cars_attributes.Count; index_car++)
            {
                CarData car = carsData.cars_attributes[index_car];
                Vector3 carPosition = new Vector3(car.x, car.y, car.z);
                newPositions.Add(carPosition);
                int randomCarIndex = Random.Range(0, carPrefabs.Length);
                carsGameObjects[index_car] = Instantiate(carPrefabs[randomCarIndex],
                                                         carPosition, Quaternion.identity);
            }
            hold = false;
        }
    }

    IEnumerator UpdateCarsData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getCarsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            carsData = JsonUtility.FromJson<CarsData>(www.downloadHandler.text);
            // Store the old positions for each agent
            oldPositions = new List<Vector3>(newPositions);
            newPositions.Clear();

            for(int index_car = 0; index_car < carsData.cars_attributes.Count; index_car++) {
                CarData car = carsData.cars_attributes[index_car];
                newPositions.Add(new Vector3(car.x, car.y, car.z));
            }
            hold = false;
        }
    }

    IEnumerator GetWorldData() 
    {
        //---------------------------------------------------------------Traffic Lights
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getTrafficLigtsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            trafficLightsData = JsonUtility.FromJson<TrafficLightsData>(www.downloadHandler.text);
            // Recieve tags from json and check for instantiation
            foreach(TrafficLightData trafficLight in trafficLightsData.traffic_light_attributes)
            {
                Instantiate(trafficLightPrefab, 
                            new Vector3(trafficLight.x, trafficLight.y, trafficLight.z), 
                            Quaternion.identity);
            }
        }
        //-----------------------------------------------------------------Destinations
        //--------------------------------------------------------------------Obstacles
        //------------------------------------------------------------------------Roads
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getTrafficLigtsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            obstacleData = JsonUtility.FromJson<ObstaclesData>(www.downloadHandler.text);
            // Recieve tags from json and check for instantiation
            foreach(ObstacleData obstacle in obstacleData.obstacles_attributes)
            {
                if (obstacle.tag == "box") {
                    Instantiate(boxPrefab, new Vector3(obstacle.x, obstacle.y, obstacle.z), Quaternion.identity);
                }
                else if (obstacle.tag == "shelf") {
                    Instantiate(shelfPrefab, new Vector3(obstacle.x, obstacle.y, obstacle.z), Quaternion.identity);
                }
                else if (obstacle.tag == "border") {
                    Instantiate(wallPrefab, new Vector3(obstacle.x, obstacle.y, obstacle.z), Quaternion.identity);
                }
            }
        }
    }

    IEnumerator UpdateWorldData()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getObstaclesEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            obstacleData = JsonUtility.FromJson<ObstaclesData>(www.downloadHandler.text);
            // Recieve tags from json and check for instantiation
            bool boxGOSurvives;

            foreach(GameObject boxGameObject in GameObject.FindGameObjectsWithTag("Box")) {
                boxGOSurvives = false;
                foreach(ObstacleData obstacle in obstacleData.obstacles_attributes)
                {
                    if (obstacle.tag == "box" && 
                        boxGameObject.transform.position.x == obstacle.x && 
                        boxGameObject.transform.position.z == obstacle.z) 
                    {
                        boxGOSurvives = true;
                    }
                }  
                if (!boxGOSurvives) {
                    Destroy(boxGameObject);
                }     
            }
        }
    }
}
