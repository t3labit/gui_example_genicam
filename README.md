# Genicam Harvesters PyQt5 gui

This is a gui that can be used to communicate with genicam camera (GIGE Vision).
This project is based on [Harvesters](https://github.com/genicam/harvesters).
This project has been tested with dalsa camera Teledyne DALSA Nano-C1920

![Gui Image Example]("./sample.png")

## Setup Python env

```
python3 -m venv env
source env/bin/activate
pip install PyQt5 harvesters opencv-python-headless
# or pip install -r requirements.txt
```
## Install Genicam GenTL 
To communicate with the GenTL Producer a cti file is required.
For this project we have use the open source **mvIMPACT_Acquire**.

Go to this website for [Linux or Windows](http://static.matrix-vision.com/mvIMPACT_Acquire/)
and download:
* install_mvGenTL_Acquire.sh
* mvGenTL_Acquire-x86_64_ABI2-2.50.1.tgz
For windows follow this [link](https://www.matrix-vision.com/manuals/mvBlueCOUGAR-XT/mvBC_section_quickstart_InstallingTheGenTLAcquirePackage.html)
Place the two file in the same folder, the run:
```
chmod a+x install_mvGenTL_Acquire.sh
./install_mvGenTL_Acquire.sh
```

You can find some tutorial of how to use Harvesters https://github.com/genicam/harvesters/blob/master/docs/TUTORIAL.rst

> Important: [Here](https://github.com/genicam/harvesters/wiki#gentl-producers) you can find other GenTL producer.


## Run 
```
start dalsa camera
cd gui
python3 gui_genicam.py

# we also provide an example to use the gui with opencv
# cd gui && python3 gui_opencv.py
```

Check **camera_genicam.py** to configure the camera parameters.

## Issue Opencv PyQt5

There is a known issue between opencv and pyqt5.
```
QObject::moveToThread: Current thread (0x564d3cfe27c0) is not the object's thread (0x564d3d544070).
Cannot move to target thread (0x564d3cfe27c0)
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "/home/manuel/python-env/env/lib/python3.10/site-packages/cv2/qt/plugins" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
Available platform plugins are: xcb, eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl.
```
If you also have this error do:
```
pip uninsall opencv-python
pip install opencv-python-headless
```


## References
* [Github harvesters](https://github.com/genicam/harvesters)
* [Intallation Harvesters](https://harvesters.readthedocs.io/en/latest/INSTALL.html#installing-python)
* [TUTORIAL ACQUISITION](https://github.com/genicam/harvesters/blob/master/docs/TUTORIAL.rst)
* [Example medium article](https://medium.com/@kshahir2004/streaming-yuv422-yuyv-packed-pixel-format-data-from-gige-vision-camera-with-python-harvesters-ee2e2aaafca0)