![Python](https://img.shields.io/badge/python-3.7-blue.svg)



# Auto-Robot
Project of driving a miniature car controlled by Raspberry Pi.



## Setup

Choose a project directory, and clone this repository.
```console
pi@raspberrypi:~$ cd Documents
pi@raspberrypi:~$ git clone https://github.com/alexBDG/Auto-Robot.git
```

Install the requirements in a custom Python environment.
```console
pi@raspberrypi:~$ python -m venv auto_env
pi@raspberrypi:~$ source auto_env/bin/activate
(auto_env) pi@raspberrypi:~$ pip install -r Auto-Robot/requirements.txt
```

Set the script to launch at startup.
```console
pi@raspberrypi:~$ sudo crontab -e
```
And add this line:
```
@reboot bash /home/pi/Documents/Auto-Robot/auto_launcher.sh
```

The best is to set a WiFi access point using the Raspberry, by following this [tutorial](https://www.tomshardware.com/how-to/raspberry-pi-access-point). It avoid using an box between the Raspberry and the controller.
To control the car, use the Android application, from the [Auto-Robot-Mobile-App](https://github.com/alexBDG/Auto-Robot-Mobile-App) repository.


## Driving
Use the script `main.py` to launch the manual driving mode.
```console
(auto_env) pi@raspberrypi:~$ python main.py -s 1. -r (200,100) --fps 20 -v 1
```

Available arguments are:

- `--help` to display the program's help message
- `--speed` to fix the car velocity
- `--resolution` to set the windows resolution
- `--fps` to set the frame per seconds value
- `--verbose` can be used to display informations if non null value


## Viewing
Launch the `vision.py` script to start an OpenCV session that open the Raspberry Camera. Quit by pressing the `q` keyboard.
```console
(auto_env) pi@raspberrypi:~$ python vision.py
```


## Autonomous mode

Connect yourself to the rasberry, start the camera and control commands (if not done at startup).

On a computer, start the reinforcement learning process:
```console
(auto_env) pi@raspberrypi:~$ cd autorobot/autonomous
(auto_env) pi@raspberrypi:~$ python env.py
```

A folder `autorobot/autonomous/results/AAAA-MM-DDTHH-MM-SS` is created and contains all output pictures.
Each picture filename is under the format `i.png` with `i` the iterration.
