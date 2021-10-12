# A Robust Head-Driven Camera Mouse System


This application offers a non-intrusive and robust HCI alternative hands-free solution to individuals unable to use a conventional mouse. Use your webcam to control your mouse with only using the movement of your head. 

## Features
* Control your mouse cursor with your head
* Three different modes for triggering mouse events: 
* Hover Mode: Hover over a point of interest while keeping still for a second. This will initiate a click.
  
* Voice Mode: Control various mouse functions using your voice with Google Speech Recognition. (Requires Internet Connection)
* Motion-only Mode: All Mouse functions are disabled. Mouse motion is enabled only.


# Getting Started

### Here is how to get the project up and running on your local machine for development purposes:

### Prerequisites



* [Visual Studio build tools](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community&rel=15#)

* [shape_predictor_68_face_landmarks.dat](https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat)





### How to Install & Run


Firstly clone the repo:

```
git clone https://cseegit.essex.ac.uk/2020_ce901/ce901_moussoulides_antonis
```

Create a virtual enviroment using venv and activate it

```
virtualenv venv
```

Then to install all the required libraries using pip, on the root directory of the project type:

```
pip install -r requirements.txt
```

Then download the ```shape_predictor_68_face_landmarks.dat``` from the prerequisites section


Inside the root directory of the project, create a folder named ```model``` and put the  ```shape_predictor_68_face_landmarks.dat``` inside the ```model``` folder

Like so: 

```
model/shape_predictor_68_face_landmarks.dat
```

Finally, run the ``gui.py`` file and choose your preffered mode of the application


## Built With

* Python 3.8



## Authors

* **Antonis Moussoulides**



## Acknowledgments

* Many thanks to Dr John Woods and Dr Liu Zilong for their valuable feedback
