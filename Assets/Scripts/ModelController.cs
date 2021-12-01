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
    public string current_direction;
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
    public string[] directions;
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
    ObstaclesData obstaclesData;
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

    private float width;
    private float height;

    void Start()
    {
        carsData = new CarsData();
        trafficLightsData = new TrafficLightsData();
        destinationsData = new DestinationsData();
        obstaclesData = new ObstaclesData();
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
        /*
        WWWForm form = new WWWForm();
        form.AddField("NAgents", NAgents.ToString());
        form.AddField("NBoxes", NBoxes.ToString());
        form.AddField("width", width.ToString());
        form.AddField("height", height.ToString());
        form.AddField("maxShelves", maxShelves.ToString());
        form.AddField("maxSteps", maxSteps.ToString());
        
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
        */
        
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + sendConfigEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            GridData gridData = JsonUtility.FromJson<GridData>(www.downloadHandler.text);
            height = gridData.height;
            width = gridData.width;
            
            StartCoroutine(GetCarsData());
            StartCoroutine(GetWorldData());
        }
        
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
                GameObject trafficLightInstance = Instantiate(trafficLightPrefab, 
                            new Vector3(trafficLight.x, trafficLight.y, trafficLight.z), 
                            Quaternion.identity);
                // for the light
                // trafficLightInstance.transform.GetChild(0).gameObject.
            }
        }
        //-----------------------------------------------------------------Destinations
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getDestinationsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            destinationsData = JsonUtility.FromJson<DestinationsData>(www.downloadHandler.text);
            // Recieve tags from json and check for instantiation
            foreach(DestinationData destinationData in destinationsData.destination_positions)
            {
                Instantiate(destinationPrefab, 
                            new Vector3(destinationData.x, destinationData.y, destinationData.z), 
                            Quaternion.identity);
                // for the light
                // trafficLightInstance.transform.GetChild(0).gameObject.
            }
        }
        //--------------------------------------------------------------------Obstacles
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getObstaclesEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            obstaclesData = JsonUtility.FromJson<ObstaclesData>(www.downloadHandler.text);
            // Recieve tags from json and check for instantiation
            foreach(ObstacleData obstacleData in obstaclesData.obstacle_positions)
            {
                // Check for better instantiation of buildings
                Instantiate(buildingPrefab,
                            new Vector3(obstacleData.x, obstacleData.y, obstacleData.z), 
                            Quaternion.identity);
                // for the light
                // trafficLightInstance.transform.GetChild(0).gameObject.
            }
        }
        //------------------------------------------------------------------------Roads
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getRoadsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            roadsData = JsonUtility.FromJson<RoadsData>(www.downloadHandler.text);
            // Recieve tags from json and check for instantiation
            foreach(RoadData roadData in roadsData.road_attributes)
            {
                // Check for roadsData.direction
                roadInstance = Instantiate(roadPrefab,
                            new Vector3(roadData.x, roadData.y, roadData.z), 
                            Quaternion.identity);
                // Scale roadInstance with widht, height and size of roadsData
            }
        }
    }

    IEnumerator UpdateWorldData()
    {
        // Update traffic lights lights
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getTrafficLigtsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            trafficLightsData = JsonUtility.FromJson<TrafficLightsData>(www.downloadHandler.text);
            // Recieve tags from json and check for instantiation

            foreach(GameObject trafficLightGameObject in GameObject.FindGameObjectsWithTag("Traffic light")) {
                foreach(TrafficLightData trafficLightData in trafficLightsData.traffic_light_attributes)
                {
                    if (trafficLightData.state) 
                    {
                        //Update light color to green
                    }
                    else
                    {
                        //Update light color to red
                    }
                }     
            }
        }
    }
}
