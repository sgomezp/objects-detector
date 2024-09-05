<p align="center">
  <img src="https://github.com/sgomezp/objects-detector/blob/dev/static/images/yolov8_logo.png" alt="Logo YOLOv8" width="100"/>
</p>



# Detection and Tracking objects in videos using YOLOv8 (Version 1.0)

## Overview
This application allows users to detect specific objects in a video using the YOLOv8 model. In version 1.0, 
the app focuses on detecting the following objects: persons, cars, trucks, buses, and traffic lights. 
Users provide a video URL, specify the start and end times for clipping the video, and the application will 
download and process the video clip, detecting and highlighting the specified objects. The processed videos 
are stored in the static/videos directory, where they can be selected and viewed by the user.

## Features
### Version 1.0
- **Object Detection**: Detects persons, cars, trucks, buses, and traffic lights in video clips using the YOLOv8 model.
- **Video Clipping**: Users can specify the start and end times to clip a specific portion of the video for processing.
- **Video Storage**: Processed video clips are saved in the static/videos directory.
- **User Interface**: Built with Flask, the web interface allows users to:
  - Input the video URL and specify clipping times.
  - Download and process the video clip for object detection.
  - View a list of saved video clips and select one to play.
### Version 2.0 (Planned)
- **Custom Object Selection**: users will be able to choose which specific objects they want to detect in the video.
- **Improved Interface:** the user interface will be enhanced to provide a more seamless and user-friendly experience.

## Installation
### Prerequisites
- **Python 3.12** (This project was developed using Python 3.12)
- **pip** (Python package installer)
- **Virtual Environment** (optional but strongly recommended)

### Setup Instructions
1. **Clone the repository**:
~~~
    git clone https://github.com/sgomezp/objects-detector.git
~~~

2. **Create and activate a virtual environment**
3. **Install dependencies**:

    Before installing dependencies, please note that the required versions of `torch` and
   `torchvision` have already been specified in the `requirements.txt` file. These versions are necessary for 
    the application to function correctly::

    - `torch` has been set to version 2.2.0
    - `torchvision` has been set to version 0.17.0

    No additional downgrades are needed; simply install the dependencies as listed in the `requirements.txt`.


~~~
     pip install -r requirements.txt
~~~

4. **Set up environment variables**:
Create a .env file in the root of the project. Inside this file, add your SECRET_KEY or other 
environment-specific variables. The SECRET_KEY is a crucial setting for Flask, as it is used for securely signing 
session cookies and enabling the use of flash messages in the application. 
Replace your_secret_key_here with a strong, unique secret key.

~~~
     SECRET_KEY=your_secret_key_here
~~~

### Model Download
Depending on your needs, you may choose from different YOLOv8 model sizes (small, medium, or large).
1. **Download the Model**: 
   - You need to download the YOLOv8 model weights that you intend to use (small, medium, or large).
   - Place the downloaded model file in the **models/** directory of your project to ensure that your application can access it.



### Run the application
~~~
    python main.py
~~~
### Access the application
Open a web browser and go to http://127.0.0.1:5000

<p align="center">
  <img src="https://github.com/sgomezp/objects-detector/blob/dev/static/images/screenshot_home.png" alt="Screeshot home" width="600"/>
</p>


## Usage
1. **Upload Video Information**:
   - Enter the YouTube video URL in the provided field.
   - Specify the start and end times of the video clip you want to process.
   - Give a name to the output video.
   - Click the "Download and Process Video" button.


2. **Process Video**:
   - The application will download the specified video clip and perform object detection using YOLOv8.
   - Upon successful processing, the video will be saved in the static/videos directory.

<p align="center">
  <img src="https://github.com/sgomezp/objects-detector/blob/dev/static/images/processed_video.png" alt="Processed video" width="600"/>
</p>


3. **View Processed Videos**:
   - Select any of the saved videos from the dropdown list to play it on the web interface


## Image Resolution Configuration
To improve processing speed, the resolution of the processed video has been reduced. The application uses the 
following format to ensure that the video is downloaded with a lower resolution.
```plaintext
format': 'bestvideo[height<=480][fps<=30]/best[height<=480][fps<=30]'
```

## Folder Structure
```plaintext
├── main.py                   # Main Flask application file
├── models                    
│   └── yolov8n.pt            # Model (not included in the repo)
├── routes                    # Flask routes
│   └── routes.py
├── processing
│   └── video_processing.py   # Video processing and object detection logic
├── static
    ├── css
│   ├── images                
│   └── videos                # Directory where processed videos are saved
├── templates
│   ├── home.html             # Home page template
│   └── show_video.html       # Video display page template
├── .env                      # Environment variables (not included in the repo)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```



## Technologies Used
- **YOLOv8**: This project uses YOLOv8, a state-of-the-art, real-time object detection system known for its speed
and accuracy. YOLOv8 is based on the YOLO (You Only Look Once) architecture and is the latest version in the YOLO 
series. This deep learning model can detect and track objects in real-time.


- **Flask**: A lightweight WSGI web application framework in Python. Flask is used to build the web interface, handle user 
inputs, and manage the application's backend processes.




