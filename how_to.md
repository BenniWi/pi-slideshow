# Prerequisits
* Download *Raspbian with Desktop*
* Download *Balena Etcher*
* Flash Linux on SD card (e.g. using Balena Etcher)

# Install applications
```sh
sudo apt-get install feh xscreensaver
```

# deactivate the screensaver using the menu
-> Menu Screensaver

# Raspberry Pi configuration
-> wait for network on boot

# create mountpoint for photos
```sudo mkdir -p /mnt/photo```

# mount network share in /etc/fstab:
```sh
sudo nano /etc/fstab
```
add entry:
```
//<ip-address>/<photo-folder> /mnt/photo cifs username=<username>,password=<password>,vers=1.0 0 0
```

# start Feh Slideshow : - run_feh_slideshow.sh in /home/pi
```
echo feh -YxqFZzr -D 30 -B black /mnt/photo/ > /home/pi/run_feh_slideshow.sh
```


## Altlernative CyclicFolder -> on every startup, another folder is used
```sh
nano /home/pi/run_feh_slideshow.sh
```
add there: 
```sh
#!/bin/bash
cyclic_path=$(python CyclicFolderSelection.py /mnt/photo/ .)
feh -YxqFZzr -D 120 -B black $cyclic_path
```

copy file **CyclicFolderSelection.py** to **/home/pi**

```sh
chmod +x /home/pi/run_feh_slideshow.sh
```

# entry in boot config for feh
```sh
mkdir -p ~/.config/autostart/
nano ~/.config/autostart/run_feh_slideshow.desktop
```
add there: 
```
[Desktop Entry]
Name=feh_slideshow
Exec=/home/pi/run_feh_slideshow.sh
Type=Application
Terminal=false
```
```sh
chmod +x ~/.config/autostart/run_feh_slideshow.desktop
```

# Listen for Shutdown
```
sudo nano listen-for-shutdown.py
```
add there:

```sh
#!/usr/bin/env python
# Idea: problem of random falling edges is solved by checking the pin twice every second
# if it is not low when checked, the shutdown call is invalid
import RPi.GPIO as GPIO
import subprocess
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while 1:
    GPIO.wait_for_edge(3, GPIO.FALLING)
    # found edge, now wait a second and check if pin is still on low signal
    time.sleep(1)
    if not GPIO.input(3):
        # pin is still on low signal, wait another second and check again
        time.sleep(1)
        if not GPIO.input(3):
            # pin is again on low voltage, break the loop and finalize the script
            break
# going to shutdown the system completely
print("Shutdown by button press -> Bye Bye")
subprocess.call(['poweroff'], shell=False) #poweroff is only solution to fully shutdown
```
```sh
sudo mv listen-for-shutdown.py /usr/local/bin/
sudo chmod +x /usr/local/bin/listen-for-shutdown.py
```

# Listen for Shutdown on Boot
```sh
sudo nano listen-for-shutdown.sh
```
add there:
```sh
#! /bin/sh

### BEGIN INIT INFO
# Provides:          listen-for-shutdown.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

# If you want a command to always run, put it here

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting listen-for-shutdown.py"
    /usr/local/bin/listen-for-shutdown.py &
    ;;
  stop)
    echo "Stopping listen-for-shutdown.py"
    pkill -f /usr/local/bin/listen-for-shutdown.py
    ;;
  *)
    echo "Usage: /etc/init.d/listen-for-shutdown.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
```
```sh
sudo mv listen-for-shutdown.sh /etc/init.d/
sudo chmod +x /etc/init.d/listen-for-shutdown.sh
sudo update-rc.d listen-for-shutdown.sh defaults
sudo /etc/init.d/listen-for-shutdown.sh start
```sh
