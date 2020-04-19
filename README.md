# spyserver_user_monitor
AirSpy Spyserver User Monitoring Utilities


## Dependencies
The following packages were required on a RPi in April 2020. YMMV.
```
$ sudo apt-get install rrdtool librrd-dev libpython3.7-dev
```

## Installation

Make a venv:
```
$ python3.7 -m venv venv
$ . venv/bin/activate
```

Install package.
```
$ pip install -r requirements.txt
$ pip install -e .
```

## Usage

```
$ cp config.yml.example config.yml
```

Edit config.yml to reflect your spyserver configuration.

Note that this script needs to be run as the same user that is running the spyservers to work correctly.

### Quick Look at Current users:
```
$ python -m spyserver_user_monitor.monitor --config=config.yml
Detected Spyservers: [5020, 5040]
Spyserver Port 5020 (20m_band): 1 users
Spyserver Port 5040 (40m_band): 0 users
```

### Create and update a rrdtool db:
```
$ python -m spyserver_user_monitor.rrdtool --update config.yml
```

### Generate Usage Graphs for each Spyserver
```
$ python -m spyserver_user_monitor.rrdtool --graphs config.yml
```

Graphs are output to the current working directory by default.