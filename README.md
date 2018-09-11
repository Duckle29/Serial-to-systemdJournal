# Serial-to-systemdJournal

This is a simple python script used to log data input on any serial port.
As it is here it's rather specialized to listening for data from ESP8266s, and will log 25 lines of erros if "reset" is seen in the text.

The script should be easilly adaptable to different use-cases.

## Dependencies

Appart from a linux installation that uses systemd, you'll also need:

* Python3
* Pyserial
* Systemd python module

To install these:

```bash
sudo apt install build-essential libsystemd-dev python3 python3-pip
pip3 install pyserial
pip3 install systemd
```

## Usage 

To use the script, you call it with three arguments:

`./log.py -p PORT -b BAUDRATE -n "LOGGER NAME"`


For example: 

`./log.py -p /dev/ttyUSB0 -b 115200 -n "Logger1"`
