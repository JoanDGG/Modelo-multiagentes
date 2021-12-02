using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.Linq;
public class ChangeCamera : MonoBehaviour
{
    // Lista de camaras vista
    private GameObject[] viewCamerasList;
    private int indexCameraViewList = 0;

    //Elementos del Canvas
    public Text textCurrentCamera;
    public Button buttonChangeCamera;
    public InputField inputCar;
    

    // Cars
    private GameObject[] carsCamerasList;
    private int indexCameraCarList = 0;

    // Start is called before the first frame update
    void Start()
    {
        if (viewCamerasList == null)                    { viewCamerasList = GameObject.FindGameObjectsWithTag("ViewCamera"); }
        //if (carsCamerasList == null)                    { carsCamerasList = GameObject.FindGameObjectsWithTag("Car").OrderBy( car => car.name ).ToArray();  }
        carsCamerasList = ModelController.carsGameObjects;

        foreach (GameObject camera in carsCamerasList)  { camera.gameObject.transform.GetChild(0).gameObject.SetActive(false); }
        foreach (GameObject camera in viewCamerasList)  { camera.SetActive(false); }
        viewCamerasList[indexCameraViewList].SetActive(true);
        textCurrentCamera.text = viewCamerasList[indexCameraViewList].name;

    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void ChangeNextView()
    {
        indexCameraViewList += 1;
        if (indexCameraViewList == viewCamerasList.Length)   { indexCameraViewList = 0; }
        
        foreach (GameObject camera in carsCamerasList)  { camera.gameObject.transform.GetChild(0).gameObject.SetActive(false); }
        foreach (GameObject camera in viewCamerasList)  { camera.SetActive(false); }
        viewCamerasList[indexCameraViewList].SetActive(true);
        textCurrentCamera.text = viewCamerasList[indexCameraViewList].name;
    }

    public void ChangeNextCar()
    {
        if ((Int32.Parse(inputCar.text) - 1) < 0 || (Int32.Parse(inputCar.text)) > carsCamerasList.Length) {
            textCurrentCamera.text = "Ingrese un número válido de coche";
        } else {
            foreach (GameObject camera in carsCamerasList)  { camera.gameObject.transform.GetChild(0).gameObject.SetActive(false); }
            foreach (GameObject camera in viewCamerasList)  { camera.SetActive(false); }
            carsCamerasList[Int32.Parse(inputCar.text) - 1].gameObject.transform.GetChild(0).gameObject.SetActive(true);
            textCurrentCamera.text = carsCamerasList[Int32.Parse(inputCar.text) - 1].name;
        }

    }

}
