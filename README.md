![Python](https://img.shields.io/badge/python-3.7-blue.svg)



# Auto-Robot
Project of driving a miniature car controlled by Raspberry Pi.



## Drive
Use the script `main.py` to launch the manual driving mode.
```console
pi@raspberrypi:~$ python main.py -s 1. -r (200,100) --fps 20 -v 1
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
pi@raspberrypi:~$ python vision.py
```


