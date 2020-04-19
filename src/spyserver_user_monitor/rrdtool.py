#
#   SpyServer User Monitor - RRDTool DB Setup and Update
#
import argparse
import logging
import os.path
import rrdtool
import sys
from .config import *
from .monitor import *



def setup_rrd(filename, config):
    """ Setup a RRDtool database, using the configuration information """
    
    # Generate arguments for rrdtool
    _args = [filename,
    "--start", "now",
    "--step", "120",
    "RRA:MAX:0.5:1:315360"]

    # Ensure db is created with metrics in a known order.
    _spyserver_list = list(config['spyservers'])
    _spyserver_list.sort()

    for _spyserver in _spyserver_list:
        _name = config['spyservers'][_spyserver]
        _args.append(f"DS:{_name}:GAUGE:120:0:100")
    
    logging.debug(f"Creating RRD DB with args: {str(_args)}")

    rrdtool.create(*_args)


def update_rrd(filename, config):
    """ Add datapoints to a RRD database """

    # Get ordered list of servers.
    _spyserver_ports = list(config['spyservers'])
    _spyserver_ports.sort()

    _spyserver_users = get_spyserver_users(_spyserver_ports)

    _cmd = "N"
    for _port in _spyserver_ports:
        _cmd += f':{len(_spyserver_users[_port])}'

    logging.debug(f"Updating db {filename} with {_cmd}")

    rrdtool.update(filename, _cmd)


def generate_graphs(filename, config, output_dir="./", periods=['h','d','w']):
    """ Output graphs for all spyservers dataseries. """
    # Get ordered list of servers.
    _spyserver_ports = list(config['spyservers'])
    _spyserver_ports.sort()

    for _port in _spyserver_ports:
        _ds_name = config['spyservers'][_port]

        for _period in periods:
            _outfile = f'{_ds_name}-1{_period}.png'

            if _period == 'h':
                _title = "%s Spyserver Usage - 1 Hour" % _ds_name.split('_')[0]
            elif _period == 'd':
                _title = "%s Spyserver Usage - 1 Day" % _ds_name.split('_')[0]
            elif _period == 'w':
                _title = "%s Spyserver Usage - 1 Week" % _ds_name.split('_')[0]
            else:
                _title = "%s Spyserver Usage" % _ds_name.split('_')[0]

            ret = rrdtool.graph( os.path.join(output_dir,_outfile),
                "--start", "-1%s" % (_period), 
                "--vertical-label=Users",
                "-w 800",
                "-g",
                "-t %s" % _title,
                "DEF:m1_num=%s:%s:MAX" % (filename, _ds_name),
                "LINE1:m1_num#0000FF:%s\r" % _ds_name)
            logging.debug(f"Wrote file: {_outfile}")


def main():
    parser = argparse.ArgumentParser(description="SpySever RRDTool Utility")
    parser.add_argument(
        "config", type=str, help="Configuration File (e.g. config.yml)"
    )
    parser.add_argument(
        "--graph", action='store_true', default=False, help="Generate graphs."
    )
    parser.add_argument(
        "--update", action='store_true', default=False, help="Update RRDtool DB with latest data."
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

    config = read_config(args.config)

    rrdfile = config['rrdtool_db']

    # Setup the RRD DB if it does not exist
    if not os.path.isfile(rrdfile):
        setup_rrd(rrdfile, config)
    else:
        logging.info("RRD DB exists, not creating.")
    
    try:
        _info = rrdtool.info(rrdfile)
        logging.info("RRD DB checked out OK.")
        logging.debug(_info)
    except Exception as exc:
        logging.exception("Error loading RRD DB", exc_info=exc)
        sys.exit(1)

    if args.update:
        update_rrd(rrdfile, config)

    if args.graph:
        generate_graphs(rrdfile, config)




if __name__ == "__main__":
    main()