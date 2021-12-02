// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz and Octavio Navarro.
// Last modified 2 December 2021

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
    public bool arrived;
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
    public List<ObstacleData> obstacles_attributes;
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

public class ModelController : MonoBehaviour
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
    List<Vector3> oldPositions;
    List<Vector3> newPositions;
    bool hold = false;

    [System.NonSerialized]
    public GameObject[] carsGameObjects;
    public GameObject[] carPrefabs = new GameObject[6];
    public GameObject[] treePrefabs = new GameObject[11];
    public GameObject trafficLightPrefab, destinationPrefab, roadPrefab, grassPrefab, cenitalCamera; // reloadButton
    public Text currentStep;
    //public int NAgents, NBoxes, width, height, maxShelves, maxSteps;
    public float timeToUpdate = 1.5f, timer, dt;

    private float width;
    private float height;
    private bool[] carsArrived;

    void Start()
    {
        carsData = new CarsData();
        trafficLightsData = new TrafficLightsData();
        destinationsData = new DestinationsData();
        obstaclesData = new ObstaclesData();
        roadsData = new RoadsData();
        oldPositions = new List<Vector3>();
        newPositions = new List<Vector3>();

        timer = 0;
        hold = true;

        InitialConfiguration();
    }

    private void Update() 
    {
        float t = timer/timeToUpdate;
        dt = t * t * ( 3f - 2f*t);

        if(timer >= timeToUpdate)
        {
            timer = 0;
            hold = true;
            StartCoroutine(UpdateSimulation());
        }

        if (!hold)
        {
            timer += Time.deltaTime;
            if(carsGameObjects.Length != 0 && oldPositions.Count != 0 && newPositions.Count != 0)
            {
                for (int s = 0; s < carsGameObjects.Length; s++)
                {
                    Vector3 interpolated = Vector3.Lerp(oldPositions[s], newPositions[s], dt);
                    carsGameObjects[s].transform.localPosition = interpolated;
                    
                    Vector3 dir = oldPositions[s] - newPositions[s];
                    if(dir != new Vector3(0, 0, 0))
                        carsGameObjects[s].transform.rotation = Quaternion.LookRotation(dir);
                }
            }
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

            int carsCount = 0;
            foreach (bool carArrived in carsArrived)
            {
                if(carArrived)
                    carsCount++;
            }
            currentStep.text = "Step " + model.currentStep 
                + "\nCars arrived " + carsCount + " / " + carsGameObjects.Length;
            if(carsCount >= carsGameObjects.Length)
            {
                currentStep.text += "\nAll cars have arrived!";
            }
            else
            {
                StartCoroutine(UpdateCarsData());
            }
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

            cenitalCamera.transform.position = new Vector3(width/2f, 20, height/2f);
            cenitalCamera.transform.rotation = Quaternion.Euler (90f, 0f, 0f);
            
            GameObject grass = Instantiate(grassPrefab, cenitalCamera.transform.position, Quaternion.identity);
            grass.transform.position = new Vector3(width/2f, 0, height/2f);
            grass.transform.localScale = new Vector3(width/8f, 1/2f, height/8f);
            ChangeCamera.viewCamerasList = GameObject.FindGameObjectsWithTag("ViewCamera");
            foreach (GameObject camera in ChangeCamera.viewCamerasList)  
            {
                camera.SetActive(false);
            }
            ChangeCamera.viewCamerasList[0].SetActive(true);
            GameObject.Find("TxtVista").GetComponent<Text>().text = ChangeCamera.viewCamerasList[0].name;
            StartCoroutine(GetCarsData());
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
            carsArrived = new bool[carsData.cars_attributes.Count];

            for (int index_car = 0; index_car < carsData.cars_attributes.Count; index_car++)
            {
                CarData car = carsData.cars_attributes[index_car];
                Vector3 carPosition = new Vector3(car.x, car.y, car.z);
                newPositions.Add(carPosition);
                int randomCarIndex = Random.Range(0, carPrefabs.Length);
                carsGameObjects[index_car] = Instantiate(carPrefabs[randomCarIndex],
                                                         carPosition, Quaternion.identity);
                carsGameObjects[index_car].name = car.unique_id.ToString();
                carsArrived[index_car] = false;
            }
            ChangeCamera.carsCamerasList = carsGameObjects;
            StartCoroutine(GetWorldData());
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
            oldPositions = new List<Vector3>(newPositions);
            newPositions.Clear();

            for(int index_car = 0; index_car < carsData.cars_attributes.Count; index_car++) {
                CarData car = carsData.cars_attributes[index_car];
                newPositions.Add(new Vector3(car.x, car.y, car.z));
                if(car.arrived)
                    carsArrived[index_car] = true;
            }
        }
        StartCoroutine(UpdateWorldData());
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
            foreach(TrafficLightData trafficLight in trafficLightsData.traffic_light_attributes)
            {
                GameObject trafficLightInstance = Instantiate(trafficLightPrefab, 
                            new Vector3(trafficLight.x, trafficLight.y, trafficLight.z), 
                            Quaternion.identity);
                trafficLightInstance.name = trafficLight.unique_id;
            }
        }
        //-----------------------------------------------------------------Destinations
        www = UnityWebRequest.Get(serverUrl + getDestinationsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            destinationsData = JsonUtility.FromJson<DestinationsData>(www.downloadHandler.text);
            foreach(DestinationData destinationData in destinationsData.destination_positions)
            {
                Instantiate(destinationPrefab, 
                            new Vector3(destinationData.x, destinationData.y, destinationData.z), 
                            Quaternion.identity);
            }
        }
        //--------------------------------------------------------------------Obstacles
        www = UnityWebRequest.Get(serverUrl + getObstaclesEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            obstaclesData = JsonUtility.FromJson<ObstaclesData>(www.downloadHandler.text);
            foreach(ObstacleData obstacleData in obstaclesData.obstacles_attributes)
            {
                int randomTreeIndex = Random.Range(0, treePrefabs.Length);
                Instantiate(treePrefabs[randomTreeIndex],
                            new Vector3(obstacleData.x, obstacleData.y, obstacleData.z), 
                            Quaternion.identity);
            }
        }
        //------------------------------------------------------------------------Roads
        www = UnityWebRequest.Get(serverUrl + getRoadsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            roadsData = JsonUtility.FromJson<RoadsData>(www.downloadHandler.text);
            foreach(RoadData roadData in roadsData.road_attributes)
            {
                if(roadData.directions.Length == 1)
                {
                    if(roadData.directions[0] == "up" || roadData.directions[0] == "down")
                    {
                        Instantiate(roadPrefab,
                                new Vector3(roadData.x, roadData.y, roadData.z), 
                                Quaternion.Euler (0f, -90f, 0f));
                    }
                    else
                    {
                        Instantiate(roadPrefab,
                                new Vector3(roadData.x, roadData.y, roadData.z), 
                                Quaternion.identity);
                    }
                }
                else
                {
                    GameObject roadInstance = Instantiate(roadPrefab,
                                new Vector3(roadData.x, roadData.y, roadData.z), 
                                Quaternion.identity);
                    roadInstance.transform.GetChild(0).gameObject.SetActive(false);
                }
            }
        }
        hold = false;
    }

    IEnumerator UpdateWorldData()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getTrafficLigtsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            trafficLightsData = JsonUtility.FromJson<TrafficLightsData>(www.downloadHandler.text);

            foreach(TrafficLightData trafficLightData in trafficLightsData.traffic_light_attributes)
            {
                GameObject trafficLightGameObject = GameObject.Find(trafficLightData.unique_id);
                if (trafficLightData.state)
                {
                    trafficLightGameObject.transform.GetChild(0)
                        .gameObject.GetComponent<Light>().color = Color.green;
                }
                else
                {
                    trafficLightGameObject.transform.GetChild(0)
                        .gameObject.GetComponent<Light>().color = Color.red;
                }
            }
        }
        hold = false;
    }
}
