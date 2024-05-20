# Keep Presence

This program will move the mouse or press a key when it detects that you are **away**.
It will pause it's action if you are using your computer.
This can be useful to keep your computer awake and stop it from powering off the monitor or entering other power saving modes.


## Demo

[![Demo](https://raw.githubusercontent.com/carrot69/keep-presence/master/demo/demo.gif)](https://github.com/carrot69/keep-presence)


# Manual installation

```
git clone https://github.com/dynbabaul/keep-presence.git

cd keep-presence

python3 -m pip install pynput

OR

apt install python3-pynput (for debian Linux this will also install the needed dependency)

python3 src/keep-presence.py
```

## Optional arguments

```
options:
  -h, --help            show this help message and exit
  -s SECONDS, --seconds SECONDS
                        Define in seconds how long to wait after a user is considered idle. Default 300.
  -p PIXELS, --pixels PIXELS
                        Set how many pixels the mouse should move. Default 1.
  -m MODE, --mode MODE  Available options: keyboard, mouse, both (mouse & keyboard) and scroll; default is mouse.
                        This is the action that will be executed when the user is idle:
                        If keyboard is selected, the program will press the shift key.
                        If mouse is selected, the program will move the mouse.
                        If both is selected, the program will do both actions.
  -r RANDOM RANDOM, --random RANDOM RANDOM
                        Usage: two numbers (ex. -r 3 10). Execute actions based on a random interval between start and stop seconds. Note: Overwrites the seconds argument.
  -t TIMEOUT, --timeout TIMEOUT
                        Define a time limit to run in  (s)econds, (m)inutes or (h)ours.
                        Example: 10s for 10 seconds, 10m for 10 minutes, 10h for 10 hours. Program will close after this amount of time.
  -ts TIMESTAMP, --timestamp TIMESTAMP
                        Define a datetime to stop running.
                        Format: CCYYMMDDhhmm
                        Example: 202405171345 for May 17th, 2024 at 1:45pm
                        Or you can use a 4 digit time for a future time to stop running.
                        The time used will be the next occurence of that time, within the next 24 hours.
                        Example: 0215 for 2:15am
                        Example: 1630 for 4:30pm


```
