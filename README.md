![Python](https://img.shields.io/badge/python-3.7-blue.svg)



# Auto-Robot
Project of driving a miniature car controlled by Raspberry Pi.



## Drive
Use the script `main.py` to launch the manual driving mode. Add an argument to specify the speed factor (normalized between 0 and 1).
```console
pi@raspberrypi:~$ python main.py 0.5
```


## Viewing
Launch the `vision.py` script to start an OpenCV session that open the Raspberry Camera. Quit by pressing the `q` keyboard.
```console
pi@raspberrypi:~$ python vision.py
```


