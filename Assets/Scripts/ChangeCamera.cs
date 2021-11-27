using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
public class ChangeCamera : MonoBehaviour
{
    // Lista de camaras
    List<GameObject> cameraList;
    public GameObject StreetCamera_1;
    public GameObject StreetCamera_2;
    public GameObject StreetCamera_3;
    public GameObject StreetCamera_4;
    public GameObject CenitalCamera;

    //Elementos del Canvas
    public Text textCurrentCamera;
    public Button buttonChangeCamera;

    private int indexCameraList = 0;

    // Start is called before the first frame update
    void Start()
    {
        cameraList = new List<GameObject>();
        cameraList.Add(StreetCamera_1);
        cameraList.Add(StreetCamera_2);
        cameraList.Add(StreetCamera_3);
        cameraList.Add(StreetCamera_4);
        cameraList.Add(CenitalCamera);
        foreach (GameObject camera in cameraList) {
            camera.SetActive(false);
        }
        cameraList[indexCameraList].SetActive(true);
        textCurrentCamera.text = cameraList[indexCameraList].name;
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void ChangeNextCamera()
    {
        indexCameraList += 1;
        if (indexCameraList == cameraList.Count) {
            indexCameraList = 0;
        }
        
        foreach (GameObject camera in cameraList) {
            camera.SetActive(false);
        }
        cameraList[indexCameraList].SetActive(true);
        textCurrentCamera.text = cameraList[indexCameraList].name;
    }
}
