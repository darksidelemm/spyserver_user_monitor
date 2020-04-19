#
#   SpyServer User Monitor
#
import logging
from .netstat import *


def get_spyserver_ports() -> list:
    """ Return a list of currently running spyserver TCP ports """

    return netstat_listeners(program_filter="spyserver").keys()


def get_spyserver_users(ports: list) -> dict:
    """ Get the lists of users connected to each supplied Spyserver port """
    _clients = netstat_users()

    _output = {}
    for _port in ports:
        if _port in _clients:
            _output[_port] = _clients[_port]
        else:
            _output[_port] = []

    return _output


def main():

    spyserver_ports = get_spyserver_ports()

    print(f"Currently Running Spyservers: {list(spyserver_ports)}")

    spyserver_users = get_spyserver_users(spyserver_ports)

    for _port in spyserver_users:
        print(f"Spyserver Port {_port}: {len(spyserver_users[_port])} users.")


if __name__ == "__main__":
    main()
