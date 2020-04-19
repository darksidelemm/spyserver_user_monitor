#
#   SpyServer User Monitor
#
import argparse
import logging
from .config import *
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

    parser = argparse.ArgumentParser(description="SpySever User Monitor")
    parser.add_argument(
        "--config", type=str, default=None, help="Configuration File (optional)"
    )
    parser.add_argument(
        "--log-level", type=str, choices=["debug", "info", "error"], default="info"
    )
    args = parser.parse_args()

    logging.basicConfig(
        format="%(asctime)s.%(msecs)03.0f [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        level=getattr(logging, args.log_level.upper()),
    )

    if args.config != None:
        config = read_config(args.config)
    else:
        config = None

    # List running Spyservers and their Ports
    spyserver_ports = get_spyserver_ports()

    print(f"Detected Spyservers: {list(spyserver_ports)}")

    spyserver_users = get_spyserver_users(spyserver_ports)

    for _port in spyserver_users:
        _description = "Unknown"
        # Get the descriptive name of this server if it exists
        if config != None:
            if _port in config['spyservers']:
                _description = config['spyservers'][_port]

        print(f"Spyserver Port {_port} ({_description}): {len(spyserver_users[_port])} users")


if __name__ == "__main__":
    main()
